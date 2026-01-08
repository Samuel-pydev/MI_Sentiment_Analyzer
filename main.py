from transformers import pipeline
import streamlit as st 
import re

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis",
                    model="cardiffnlp/twitter-roberta-base-sentiment")

sentiment = load_model()

def analyse_mixed_sentiment(text):
    
    sentences = re.split(r'[.!?]+|\bbut\b|\bhowever\b|\bthough\b|\balthough\b',text)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 5]
    
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

st.title("NIG Sentiment Analyzer")
st.write("Analyze sentiment in Nigerian social media text")

tab1, tab2, tab3 = st.tabs(["Single text", "Batch Analysis", "testing Phrase"])

with tab1:
    user_input = st.text_area("Enter text to analyze:", height=100)

    if st.button("Analyze Sentiment", key="single"):
        if user_input:
            # Analyze
            result = sentiment(user_input)[0]
            sentiment_label = label_map[result['label']]
            confidence = result['score']
            
            # Display results
            st.subheader("Results:")    
            st.info(f"**Text:** ' {user_input} '")
            st.info(f"**Sentiment:** {sentiment_label}")
            st.info(f"**Confidence:** {confidence:.2%}")
        else:
            st.warning("Please enter some text first")

with tab2:
    st.write("Enter multiple texts (one per line):")
    batch_input = st.text_area("Paste comments here:", height=200, key="batch")
    
    if st.button("Analyze All", key="batch_btn"):
        if batch_input:
            # Split by newlines and filter empty lines
            texts = [ # TODO 
                    line.strip() # get rid of white spaces in the line
                   for line in batch_input.split('\n')  # for lines in the input split them at a new line ??? i get what it does but can't explain it 
                        if line.strip()
                    ]
            
            if texts: # if text is not empty
                st.write(f"Analyzing {len(texts)} texts...") # shows a text saying analyzing with the number of text/sentences 
                
                # Analyze each text
                results = [] # results equals an empty list
                for text in texts:
                    result = sentiment(text)[0]  
                    results.append({ # append adds data to the end of a list 
                        'text': text,
                        'sentiment': label_map[result['label']],
                        'confidence': result['score']
                    })
                
                # Show summary stats
                st.subheader("Summary:")
                positive = sum(1 for analysis in results if analysis['sentiment'] == 'Positive') # assigns 1 to be added for the ampunt of r in results 
                negative = sum(1 for analysis in results if analysis['sentiment'] == 'Negative')
                neutral = sum(1 for analysis in results if analysis['sentiment'] == 'Neutral')
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Positie", positive)
                col2.metric("Negative", negative)
                col3.metric("Neutral", neutral)
                
                # Show individual results
                st.subheader("Individual Results:")
                for num, analysis in enumerate(results, 1): # enumerate to get the index and the item  , and the number is to tell it to start from 1
                    with st.expander(f"{num}. {analysis['sentiment']} ({analysis['confidence']:.1%})"):
                        st.write(analysis['text'])
            else:
                st.warning("No valid texts found")
        else:
            st.warning("Please enter some texts first")
            
            
    with tab3:
         st.write(" Hello Wrold ")
