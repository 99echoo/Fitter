# AI API Setup Guide

This guide explains how to obtain and configure API keys for the Fitter AI services.

## Prerequisites

- Python 3.11+ installed
- Poetry package manager
- Active accounts for OpenAI and Kling AI

## OpenAI GPT-Image 1.5

### Step 1: Obtain API Key

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign in with your OpenAI account
3. Navigate to **API keys**
4. Click **Create new secret key**
5. Copy the generated API key

### Step 2: Configure Billing (if required)

- For production use, ensure billing is enabled
- Visit [Billing](https://platform.openai.com/account/billing)
- Add a payment method if needed

### Step 3: Verify Model Access

The model we use is:
- **Model ID**: `gpt-image-1.5`
- **Capability**: High-quality image generation and editing
- **Output**: Base64-encoded image data

### Pricing

- See [OpenAI pricing](https://openai.com/pricing) for current image generation rates
- Use small-scale tests before production rollout

## Kling AI Image-to-Video API

### Step 1: Obtain Access Key / Secret Key

1. Visit the Kling AI developer portal
2. Create an Access Key and Secret Key
3. Store both keys securely

### Step 2: Verify Model Name

The default model is:
- **Model ID**: `kling-v1` (configurable)
- **Other options**: `kling-v1-6`, `kling-v2-5-turbo`, `kling-v2-6`, etc.

If you get authentication or model errors, verify the correct model name from the Kling docs.

## Environment Configuration

### Step 1: Create .env File

If not already present, copy the template:

```bash
cp .env.example .env
```

### Step 2: Add API Keys

Edit `/Users/dh/Desktop/Fitter/.env`:

```env
# OpenAI GPT-Image API
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_IMAGE_MODEL=gpt-image-1.5

# Optional (multiple orgs/projects)
OPENAI_ORG_ID=your_openai_org_id_here
OPENAI_PROJECT_ID=your_openai_project_id_here

# Optional OpenAI image settings
OPENAI_IMAGE_OUTPUT_SIZE=1024x1536
OPENAI_IMAGE_OUTPUT_FORMAT=png
OPENAI_IMAGE_QUALITY=auto
OPENAI_IMAGE_N=1  # 1-5 supported

# Kling AI Image-to-Video API
KLING_ACCESS_KEY=your_kling_access_key_here
KLING_SECRET_KEY=your_kling_secret_key_here

# Optional Kling settings
KLING_BASE_URL=https://api-singapore.klingai.com
KLING_MODEL_NAME=kling-v1
KLING_MODE=pro
KLING_DURATION=5

# Optional fallback (legacy)
KLING_API_KEY=your_kling_access_key_here

# Database (already configured)
DATABASE_URL=postgresql://fitter:fitter_password@localhost:5432/fitter

# Other settings (keep as is)
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

### Step 3: Verify Configuration

Run the verification scripts:

```bash
cd backend

# Test OpenAI GPT-Image API
poetry run python scripts/test_gpt_image.py

# Test Kling AI API
poetry run python scripts/test_kling_ai.py
```

## API Rate Limits and Quotas

### OpenAI

- **Rate limits**: Vary by account tier and model
- Monitor usage in the OpenAI dashboard
- Add billing for higher limits

### Kling AI

- **Rate Limits**: Varies by account tier
- **Queue System**: Tasks are queued and processed asynchronously
- **Timeout**: Video generation can take several minutes

## Cost Estimates

### For Development/Testing
- Image generations: see OpenAI pricing
- Video generations: see Kling pricing

### For Production (per user interaction)
- 1 try-on image: see OpenAI pricing
- 1 360° video: see Kling pricing

## Troubleshooting

### OpenAI API Issues

**Error: "Incorrect API key provided"**
- Verify the key is correct in `.env`
- Check if the API key has required permissions
- Ensure billing is enabled if needed

**Error: "Model not found"**
- Model name should be `gpt-image-1.5`
- Verify your account has access to GPT Image models

**Error: "Quota exceeded"**
- You've hit your usage limits
- Add billing or wait for quota reset
- Monitor usage in the OpenAI dashboard

### Kling API Issues

**Error: "Invalid API key"**
- Verify the access/secret keys in `.env`
- Ensure no extra spaces or quotes
- Regenerate keys if necessary

**Error: "Model not available"**
- Verify `model_name` is correct
- Update `KLING_MODEL_NAME` if needed

**Error: "Invalid input image"**
- Use a public image URL or a valid local file
- Ensure the file is a supported image format

**Error: "Timeout"**
- Video generation can take several minutes
- Retry the request or test with shorter duration

## Security Best Practices

1. **Never commit .env file** - It's in `.gitignore` already
2. **Rotate keys regularly** - Especially after sharing code
3. **Use environment-specific keys** - Different keys for dev/staging/prod
4. **Monitor usage** - Set up billing alerts
5. **Restrict key permissions** - Use minimum required scopes

## Additional Resources

- [OpenAI Images API Docs](https://platform.openai.com/docs/api-reference/images)
- [OpenAI Image Generation Guide](https://platform.openai.com/docs/guides/image-generation)
- [Kling AI Documentation](https://api-singapore.klingai.com)

## Support

If you encounter issues:
1. Check error messages carefully
2. Verify API keys and model names
3. Review official API documentation
4. Check API status pages
5. Contact API provider support if needed
