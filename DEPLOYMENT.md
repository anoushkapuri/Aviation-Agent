# Deployment Guide - Permanent Domain Name

## Option 1: Streamlit Cloud (Recommended - Free)

### Steps:
1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Go to [share.streamlit.io](https://share.streamlit.io)**
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `Aviation-Agent`
   - Set main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Set up environment variables**
   - In the Streamlit Cloud dashboard, go to your app settings
   - Add your `OPENAI_API_KEY` as a secret
   - The app will get a permanent URL like: `https://your-app-name.streamlit.app`

## Option 2: Railway (Alternative - Free tier available)

### Steps:
1. **Go to [railway.app](https://railway.app)**
2. **Connect your GitHub repository**
3. **Add environment variables:**
   - `OPENAI_API_KEY`: Your OpenAI API key
4. **Deploy** - Railway will give you a permanent URL

## Option 3: Heroku (Paid)

### Steps:
1. **Create a `Procfile`:**
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy to Heroku:**
   ```bash
   heroku create your-app-name
   heroku config:set OPENAI_API_KEY=your_api_key
   git push heroku main
   ```

## Option 4: Custom Domain (Advanced)

### For any of the above platforms:
1. **Purchase a domain** (e.g., from Namecheap, GoDaddy)
2. **Configure DNS** to point to your app's URL
3. **Set up SSL certificate** (usually automatic)

## Environment Variables Required:
- `OPENAI_API_KEY`: Your OpenAI API key

## File Structure for Deployment:
```
Aviation-Agent/
├── streamlit_app.py      # Main app file
├── agent.py             # Agent logic
├── pdf_processor.py     # PDF processing
├── requirements.txt     # Dependencies
├── .streamlit/          # Streamlit config
│   └── config.toml
├── test_pdfs/           # Your PDF documents
└── README.md
```

## Notes:
- **Streamlit Cloud** is the easiest option with a free permanent URL
- **PDFs in test_pdfs** will be included in the deployment
- **Environment variables** keep your API key secure
- **Custom domains** can be added to any platform

## Quick Deploy Command (Streamlit Cloud):
```bash
# After pushing to GitHub
streamlit deploy streamlit_app.py
``` 