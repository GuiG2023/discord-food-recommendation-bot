
A full-stack learning project incorporating asynchronous programming, cache optimization, and distributed system design.
# Discord Food Recommendation Bot

A full-stack learning project demonstrating asynchronous programming, cache optimization, and distributed system design.

## Quick Start

### Prerequisites
- Python 3.11+
- Docker & docker-compose
- Discord Bot Token
- Yelp API Key

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/GuiG2023/discord-food-recommendation-bot.git
cd discord-food-recommendation-bot

# 2. Create .env file
cp .env.example .env
# Edit .env and add your credentials

# 3. Start local services
docker-compose up -d

# 4. Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Run the Bot
python -m bot.main
```

## Project Structure
discord-food-recommendation-bot/
├── bot/                  # Discord Bot layer
├── api/                  # FastAPI backend
├── db/                   # Database operations
├── cache/                # Redis caching layer
├── tasks/                # Celery async tasks
├── tests/                # Unit tests
├── docs/                 # Documentation
├── deploy/               # Docker configs
├── scripts/              # Utility scripts
├── docker-compose.yml    # Local orchestration
├── requirements.txt      # Python dependencies
└── .env.example          # Environment template
## Documentation

- [Design Document](docs/DESIGN.md) - Complete architecture and API specs

## Development Phases

- Phase 1: MVP (search + pagination)
- Phase 2: Database integration
- Phase 3: Cache optimization
- Phase 4: Async architecture
- Phase 5: Production deployment
- Phase 6: Documentation

## Tech Stack

- **Bot**: discord.py 2.x
- **Backend**: FastAPI 0.129.0
- **Cache**: Redis 7.x
- **Queue**: Celery 5.x
- **Database**: MySQL 8.0
- **Deploy**: Docker + docker-compose

## Performance Targets

- Cache hit: <100ms
- API response: 400-600ms
- Total response: <1s
- Hit ratio: >90%
- Concurrent users: 100+
- Cost: $0

## License

MIT
