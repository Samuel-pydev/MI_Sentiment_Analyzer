from transformers import pipeline
import streamlit as st 
import re

token = st.secrets.get("HF_TOKEN", None)

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis",
                    model="cardiffnlp/twitter-roberta-base-sentiment",
                    token=token 
                    )

sentiment = load_model()

def analyze_mixed_sentiment(text):
    
    sentences = re.split(r'[.,!?]+|\bbut\b|\bhowever\b|\bthough\b|\balthough\b|\band\b',text)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 5]
    
    if len(sentences) <= 1:
        return None
    
    if len(sentences) <= 1:
        return None
    
    sentence_results = []
    for sentence in sentences:
        result = sentiment(sentence)[0]
        sentence_results.append({
            'text': sentence,
            'sentiment': label_map[result['label']],
            'confidence': result['score']
        })
    
    # Check if there's an actual sentiment
    sentiments_found = set(s['sentiment'] for s in sentence_results)
    has_positive = 'Positive' in sentiments_found
    has_negative = 'Negative' in sentiments_found

    
    if has_positive and has_negative:
        return sentence_results
    else:
        return None

# Lable assignment
label_map = {
    'LABEL_0':'Negative',
    'LABEL_1':'Neutral',
    'LABEL_2':'Positive',
}


# Streamlit UI

st.title("Sentiment Analyzer")
st.write("Analyze sentiment in Nigerian social media text")

tab1, = st.tabs([ "Batch Analysis"])

with tab1:
    st.write("Enter multiple texts (one per line):")
    batch_input = st.text_area("Paste comments here:", height=200, key="batch")
    
    if st.button("Analyze All", key="batch_btn"):
        if batch_input:
            # Split by newlines and filter empty lines
            texts = [line.strip() for line in batch_input.split('\n') if line.strip()]
            
            if texts:
                st.write(f"Analyzing {len(texts)} texts...")
                
                # Analyze each text
                results = []
                mixed_results = []
                
                for text in texts:
                    # Check if mixed first
                    mixed_analysis = analyze_mixed_sentiment(text)
                    
                    if mixed_analysis:
                        # Store mixed sentiment separately
                        mixed_results.append({
                            'original_text': text,
                            'breakdown': mixed_analysis
                        })
                        # For summary, count as mixed
                        results.append({
                            'text': text,
                            'sentiment': 'Mixed',
                            'confidence': 0.5
                        })
                    else:
                        # Regular sentiment
                        result = sentiment(text)[0]
                        results.append({
                            'text': text,
                            'sentiment': label_map[result['label']],
                            'confidence': result['score']
                        })
                
                # Show summary stats
                st.subheader("Summary:")
                positive = sum(1 for analysis in results if analysis['sentiment'] == 'Positive')
                negative = sum(1 for analysis in results if analysis['sentiment'] == 'Negative')
                neutral = sum(1 for analysis in results if analysis['sentiment'] == 'Neutral')
                mixed = sum(1 for analysis in results if analysis['sentiment'] == 'Mixed')
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Positive", positive)
                col2.metric("Negative", negative)
                col3.metric("Neutral", neutral)
                col4.metric("Mixed", mixed)
                
                # Show mixed sentiment details first if any
                if mixed_results:
                    st.subheader("Mixed Sentiment Texts:")
                    with st.expander(f"Mixed ({len(mixed_results)})"):
                        for idx, item in enumerate(mixed_results, 1):
                            st.write(f"**{idx}. {item['original_text']}**")
                            st.write("Breakdown:")
                            for part in item['breakdown']:
                                st.write(f"  - {part['sentiment']} ({part['confidence']:.1%}): _{part['text']}_")
                            st.write("")
                
                # Group results by sentiment
                st.subheader("Individual Results:")
                positive_texts = [r for r in results if r['sentiment'] == 'Positive']
                negative_texts = [r for r in results if r['sentiment'] == 'Negative']
                neutral_texts = [r for r in results if r['sentiment'] == 'Neutral']
                
                # Show grouped dropdowns
                if positive_texts:
                    with st.expander(f"Positive ({len(positive_texts)})"):
                        for analysis in positive_texts:
                            st.write(f"- {analysis['text']} ({analysis['confidence']:.1%})")

                if negative_texts:
                    with st.expander(f"Negative ({len(negative_texts)})"):
                        for analysis in negative_texts:
                            st.write(f"- {analysis['text']} ({analysis['confidence']:.1%})")

                if neutral_texts:
                    with st.expander(f"Neutral ({len(neutral_texts)})"):
                        for analysis in neutral_texts:
                            st.write(f"- {analysis['text']} ({analysis['confidence']:.1%})")
            else:
                st.warning("No valid texts found")
        else:
            st.warning("Please enter some texts first")
            



