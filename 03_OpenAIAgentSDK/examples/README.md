# Examples

## Weather Agent

A simple AI agent that fetches real-time weather data using OpenWeather API.

### Setup

1. **Get OpenWeather API Key** (FREE)
   - Go to: https://openweathermap.org/api
   - Sign up and get your free API key

2. **Add to .env file:**
   ```
   OPENWEATHER_API_KEY=your-key-here
   GROQ_API_KEY=your-groq-key  # or OPENAI_API_KEY
   ```

3. **Install dependencies:**
   ```bash
   pip install requests
   ```

### Run

```bash
python examples/weather_agent.py
```

### Example Queries

- "What's the weather in London?"
- "How's the weather in Tokyo today?"
- "Tell me about the weather in New York"

### Features

- ✅ Real-time weather data
- ✅ Temperature in Celsius
- ✅ Weather conditions
- ✅ Humidity and wind speed
- ✅ Clean, single-file implementation
- ✅ Error handling
