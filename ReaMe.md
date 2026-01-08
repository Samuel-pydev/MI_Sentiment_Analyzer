#  Sentiment Analyzer

A sentiment analysis tool that analyzes text and detects positive, negative, neutral, and mixed sentiments.

## Features

- **Single Text Analysis**: Analyze individual texts with confidence scores
- **Batch Analysis**: Analyze multiple texts at once with summary statistics
- **Mixed Sentiment Detection**: Automatically detects and breaks down texts with conflicting sentiments
- **Grouped Results**: Results organized by sentiment type for easy review

## How to Use

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

3. Enter text to analyze:
   - For single analysis: Enter one text in the input box
   - For batch analysis: Enter multiple texts (one per line)

## Technology

- **Model**: CardiffNLP Twitter RoBERTa Base Sentiment
- **Framework**: Streamlit
- **NLP Library**: Hugging Face Transformers

## Limitations

- Mixed sentiment detection works best with clear positive/negative contrasts (e.g., "great but terrible")
- May not catch subtle or context-dependent sentiments
- Works primarily on English text

## Future Improvements

- Add support for Nigerian pidgin phrases
- Improve mixed sentiment detection accuracy
- Add data export functionality