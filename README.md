# Mobile Game Analytics and Prediction Platform

A comprehensive machine learning system that predicts mobile game success metrics using scraped data from app stores. The platform combines web scraping, classification algorithms, learning-to-rank techniques, and a web interface to provide game analytics and performance predictions.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [API Reference](#api-reference)
- [Machine Learning Pipeline](#machine-learning-pipeline)
- [Web Interface](#web-interface)
- [Development](#development)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Overview

This system provides two main services:
1. **Game Performance Prediction**: Predict download ranges and rankings for games based on their attributes
2. **Optimal Attribute Recommendations**: Suggest optimal game attributes to achieve desired performance criteria

The platform processes data from over 40,000 mobile games to provide accurate predictions using advanced machine learning techniques.

## Features

- **Web Scraping Pipeline**: Automated data collection from 42matters.com using Selenium and BeautifulSoup
- **Machine Learning Prediction**: GradientBoostingClassifier for download tier classification
- **Learning-to-Rank System**: RankLib integration for genre-based game ranking
- **Trend Analysis Engine**: Statistical analysis for optimal attribute recommendations  
- **Interactive Web Interface**: AngularJS frontend with real-time predictions
- **Comprehensive Database**: MySQL storage with structured game metadata
- **Cross-Validation Testing**: Model accuracy optimization across multiple algorithms

## System Architecture

```
┌─────────────────────┐    ┌──────────────────────┐    ┌─────────────────────┐
│   Data Collection   │    │   Processing Layer   │    │   Prediction API    │
│                     │    │                      │    │                     │
│ ┌─────────────────┐ │    │ ┌──────────────────┐ │    │ ┌─────────────────┐ │
│ │ scrape.py       │ │    │ │ rough.py         │ │    │ │ server.py       │ │
│ │ (Selenium)      │ │────┤ │ (Score Calc)     │ │────┤ │ (Prediction)    │ │
│ └─────────────────┘ │    │ └──────────────────┘ │    │ └─────────────────┘ │
│                     │    │                      │    │                     │
│ ┌─────────────────┐ │    │ ┌──────────────────┐ │    │ ┌─────────────────┐ │
│ │ crawler.php     │ │    │ │ rank.py          │ │    │ │ server2.py      │ │
│ │ (Detail Scrape) │ │    │ │ (Genre Ranking)  │ │    │ │ (Analysis)      │ │
│ └─────────────────┘ │    │ └──────────────────┘ │    │ └─────────────────┘ │
└─────────────────────┘    └──────────────────────┘    └─────────────────────┘
                                      │
                             ┌──────────────────────┐
                             │   MySQL Database     │
                             │                      │
                             │ • url               │
                             │ • games             │ 
                             │ • games_formatted   │
                             │ • scores            │
                             │ • ranked_games      │
                             └──────────────────────┘
```

## Installation

### Prerequisites

- Python 2.7
- MySQL Server
- Java Runtime Environment (JRE) 8+
- Firefox WebDriver
- PHP with simple_html_dom library

### System Dependencies

```bash
# Install MySQL
# macOS
brew install mysql

# Ubuntu
sudo apt-get install mysql-server

# Install Java
# macOS  
brew install openjdk@8

# Ubuntu
sudo apt-get install openjdk-8-jre

# Install PHP
# macOS
brew install php

# Ubuntu
sudo apt-get install php php-mysql
```

### Python Dependencies

```bash
# Install required Python packages
pip install scikit-learn==0.18.2
pip install pandas==0.20.3
pip install selenium==3.141.0
pip install beautifulsoup4==4.6.0
pip install MySQL-python==1.2.4
```

### Database Setup

1. Create MySQL database:
```sql
CREATE DATABASE dataset;
USE dataset;

-- Create required tables
CREATE TABLE url (
    id INT PRIMARY KEY,
    game_name VARCHAR(255),
    game_url TEXT,
    price FLOAT
);

CREATE TABLE games (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    genre VARCHAR(100),
    rating FLOAT,
    rating_count INT,
    date VARCHAR(50),
    size FLOAT,
    downloads VARCHAR(100),
    price FLOAT
);

CREATE TABLE games_formatted (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    genre VARCHAR(100),
    rating FLOAT,
    rating_count INT,
    date VARCHAR(50),
    size FLOAT,
    downloads VARCHAR(50),
    price FLOAT
);

CREATE TABLE scores (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    genre INT,
    size FLOAT,
    price FLOAT,
    rating FLOAT,
    review_count INT,
    downloads INT,
    score FLOAT
);

CREATE TABLE ranked_games (
    id INT PRIMARY KEY,
    rank INT,
    name VARCHAR(255),
    genre INT,
    size FLOAT,
    price FLOAT,
    rating FLOAT,
    review_count INT,
    downloads INT,
    score FLOAT
);
```

2. Update database credentials in configuration files:
```python
# Update in all Python files:
db = MySQLdb.connect(
    user='root',
    passwd='your_password',  # Change from 'suna'
    db='dataset',
    host='localhost'
)
```

### Download WebDriver

```bash
# Download Firefox GeckoDriver
# macOS
brew install geckodriver

# Ubuntu
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
tar -xzf geckodriver-v0.26.0-linux64.tar.gz
sudo mv geckodriver /usr/local/bin/
```

### Project Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Machine-Learning-Project
```

2. Update file paths in configuration:
   - Update CSV path in `Server/server.py` and `Server/Max_Accuracy.py`
   - Update RankLib jar path in `Server/server.py`
   - Verify all absolute paths match your system

## Usage

### Starting the Services

1. **Start the Prediction Engine** (Port 8000):
```bash
cd Server
python server.py
```

2. **Start the Analysis Engine** (Port 8001):
```bash
cd Server
python server2.py
```

3. **Serve the Web Interface**:
```bash
# Using Python's built-in server
cd "Executable UI"
python -m SimpleHTTPServer 8080
# Visit: http://localhost:8080/bark.html
```

### Data Collection Workflow

1. **Scrape Basic Game Data**:
```bash
cd Scraper
python scrape.py
```

2. **Crawl Detailed Metadata**:
```bash
cd Scraper
php crawler.php
```

3. **Process and Score Games**:
```bash
cd Ranking
python rough.py
```

4. **Generate Rankings by Genre**:
```bash
cd Ranking
python rank.py
```

### Machine Learning Operations

1. **Compare Algorithm Performance**:
```bash
cd Server
python Max_Accuracy.py
```

2. **Run Cross-Validation**:
```bash
cd Server
python cross_validation.py
```

3. **Train Ranking Model**:
```bash
cd Ranking
java -jar RankLib-2.1-patched.jar -train dummy.txt -save mymodel.txt
```

## Database Schema

### Primary Tables

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `url` | Scraped URLs | id, game_name, game_url, price |
| `games` | Raw game metadata | id, title, genre, rating, rating_count, size, downloads |
| `games_formatted` | Processed game data | id, title, genre, rating, rating_count, size, downloads |
| `scores` | Games with ML scores | id, name, genre, size, price, rating, review_count, downloads, score |
| `ranked_games` | Final ranked games | id, rank, name, genre, size, price, rating, review_count, downloads, score |

### Data Flow

```
Raw URLs → Detailed Scraping → Formatting → Scoring → Ranking
   ↓              ↓               ↓          ↓         ↓
  url    →     games     →  games_formatted → scores → ranked_games
```

## API Reference

### Prediction API (Port 8000)

**Endpoint**: `POST http://localhost:8000/`

**Request Parameters**:
- `name`: Game name (optional)
- `genre`: Genre ID (0-19)
- `size`: Game size (float)
- `sizeType`: Size unit ('mb' or 'gb')
- `price`: Game price (float)
- `rating`: Average rating (float, 1-5)
- `review_count`: Number of reviews (integer)

**Response**: `{download_range};{estimated_rank}`

**Example**:
```bash
curl -X POST http://localhost:8000/ \
  -d "name=TestGame&genre=2&size=25&sizeType=mb&price=0.99&rating=4.2&review_count=1000"
```

**Response**: `"1,000,000 - 10,000,000;1205"`

### Analysis API (Port 8001)

**Endpoint**: `POST http://localhost:8001/`

**Request Parameters**:
- `name`: Game name (optional)
- `genre`: Target genre ID (0-19, -1 for any)
- `downloads`: Target download tier (0-4, -1 for any)
- `rank`: Target rank threshold (-1 for any)

**Response**: `{size};{rating};{review_count};{genre};{download_distribution}`

## Machine Learning Pipeline

### Feature Engineering

**Input Features**:
- `genre`: Game category (0-19)
- `size`: Game size in MB
- `price`: Game price in USD  
- `rating`: Average user rating (1-5)
- `review_count`: Total number of reviews

**Target Variable**: `downloads` (classified into 5 tiers)

### Classification Tiers

| Tier | Download Range | Description |
|------|---------------|-------------|
| 0 | < 100,000 | Very Low |
| 1 | 100,000 - 1,000,000 | Low |
| 2 | 1,000,000 - 10,000,000 | Medium |
| 3 | 10,000,000 - 100,000,000 | High |
| 4 | 100,000,000 - 1,000,000,000 | Very High |

### Genre Categories (0-19)

Action, Adventure, Arcade, Board, Brain Games, Card, Casino, Casual, Creativity, Educational, Music, Pretend Play, Puzzle, Racing, Role Playing, Simulation, Sports, Strategy and Tools, Trivia, Word

### Model Performance

The system evaluates four algorithms:
- **DecisionTreeClassifier**: Basic tree-based classification
- **RandomForestClassifier**: Ensemble of decision trees  
- **ExtraTreesClassifier**: Extremely randomized trees
- **GradientBoostingClassifier**: Sequential boosting (selected for production)

**Production Model**: GradientBoostingClassifier
- `n_estimators=100`: Number of boosting stages
- `learning_rate=1.0`: Learning rate shrinks contribution
- `max_depth=None`: Maximum tree depth  
- `random_state=0`: Reproducible results

**Training Configuration**:
- Training samples: 37,500 games
- Test samples: Remaining games from 40K+ dataset
- Data source: `/Ranking/data40Ksklearn.csv`

### Learning-to-Rank Integration

The system uses RankLib for learning-to-rank:

1. **Feature Format**: `target qid:genre 1:size 2:price 3:rating 4:reviews`
2. **Training**: Java-based RankLib model training
3. **Scoring**: Generates relevance scores for ranking

## Web Interface

### BARK Inc. Frontend

**Technology Stack**:
- AngularJS 1.x
- Bootstrap 3.x
- jQuery 2.2.1
- WOW.js animations
- Custom CSS styling

### Two Main Interfaces

#### 1. Game Performance Prediction ("I have a Game in Mind")
- Input game attributes (genre, size, price, rating, reviews)
- Real-time prediction with progress animation
- Download range prediction and estimated rank
- Visual feedback with animated circles

#### 2. Attribute Recommendations ("Need attrs for a new Game")  
- Specify desired performance criteria (downloads, genre, rank)
- Statistical trend analysis
- Optimal attribute recommendations
- Download distribution visualization

### User Experience Features
- Smooth scroll navigation
- WOW.js entrance animations
- Responsive Bootstrap layout
- Real-time AJAX predictions
- Interactive progress indicators
- Tooltip guidance

## Development

### Project Structure

```
Machine-Learning-Project/
├── Server/                     # ML prediction engines
│   ├── server.py              # Main prediction API (port 8000)
│   ├── server2.py             # Analysis API (port 8001)
│   ├── Max_Accuracy.py        # Algorithm comparison
│   ├── cross_validation.py    # Model validation
│   └── test.txt               # Ranking test data
├── Scraper/                   # Data collection
│   ├── scrape.py             # Selenium scraper
│   └── crawler.php           # Detail crawler
├── Ranking/                   # ML ranking system
│   ├── rough.py              # Score calculation
│   ├── rank.py               # Genre-based ranking
│   ├── data40Ksklearn.csv    # Training dataset (40K+ games)
│   ├── RankLib-2.1-patched.jar  # Learning-to-rank library
│   ├── dummy.txt             # Training data for ranking
│   ├── mymodel.txt           # Trained ranking model
│   └── mysco.txt             # Model scores
├── Executable UI/             # Web interface
│   ├── bark.html             # Main frontend
│   └── files/                # Static assets
│       ├── css/              # Stylesheets
│       ├── js/               # JavaScript
│       └── fonts/            # Typography
├── ScreenShots/              # Application screenshots
└── MySQL-python-1.2.4b4/    # Database connector
```

### Development Workflow

1. **Data Collection**: Run scrapers to gather new game data
2. **Data Processing**: Process raw data into ML-ready format
3. **Model Training**: Train and validate prediction models
4. **Ranking Generation**: Create genre-based rankings  
5. **API Testing**: Verify prediction and analysis endpoints
6. **Frontend Integration**: Test web interface functionality

### Configuration Management

**Key Configuration Files**:
- Database credentials: Update in all Python files
- File paths: Update absolute paths for your system
- API endpoints: Configured in `app.js` for frontend
- Model parameters: Adjust in respective Python files

### Adding New Features

1. **New Algorithms**: Extend `Max_Accuracy.py` with additional classifiers
2. **Additional Features**: Modify feature extraction in data processing scripts
3. **New Genres**: Update genre mappings in both backend and frontend
4. **Enhanced UI**: Extend AngularJS controllers and templates

## Screenshots

The `ScreenShots/` directory contains application screenshots:
- `landing page.png`: Main interface
- `Database.png`: Database structure
- `MART Begin.png` / `MART Completed.png`: Model training process
- `prediction server_ start.png`: Server startup
- `Type1_*.png`: Game prediction interface
- `Type2_*.png`: Attribute recommendation interface

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Update absolute paths in configuration files
4. Test data pipeline and prediction accuracy
5. Commit changes (`git commit -am 'Add new feature'`)
6. Push to branch (`git push origin feature/new-feature`)
7. Create Pull Request

### Development Guidelines

- Maintain Python 2.7 compatibility
- Update database schema migrations
- Add comprehensive error handling
- Test ML model performance impact
- Document API changes
- Verify frontend compatibility

## Technical Specifications

### Performance Metrics
- **Dataset Size**: 40,000+ mobile games
- **Training Speed**: ~2-3 minutes on modern hardware
- **Prediction Latency**: <1 second per request
- **Accuracy**: Optimized through cross-validation testing

### Scalability Considerations
- **Database**: MySQL with indexed queries for fast lookups
- **Concurrent Users**: Limited by single-threaded Python HTTP servers
- **Data Updates**: Batch processing for new game data integration
- **Model Retraining**: Offline process with model replacement

### Security Notes
- Database credentials hardcoded (development only)
- No authentication on API endpoints
- CORS enabled for cross-origin requests
- Input validation limited

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Verify MySQL server is running
   - Check credentials in Python files
   - Ensure database 'dataset' exists

2. **Selenium WebDriver Issues**:
   - Update Firefox WebDriver version
   - Check browser compatibility
   - Verify WebDriver in system PATH

3. **Java RankLib Errors**:
   - Confirm Java JRE 8+ installed
   - Check RankLib jar file path
   - Verify input data format

4. **Python Import Errors**:
   - Install required packages with pip
   - Check Python 2.7 compatibility
   - Verify package versions

### Performance Optimization

- **Database Indexing**: Add indexes on frequently queried columns
- **Caching**: Implement Redis for prediction caching  
- **Load Balancing**: Deploy multiple API server instances
- **Async Processing**: Convert to async Python framework

## Future Enhancements

### Planned Features
- Real-time data streaming from app stores
- Advanced deep learning models (TensorFlow/PyTorch)
- Multi-platform support (iOS, web games)
- RESTful API with authentication
- Real-time recommendation updates
- A/B testing framework for model comparison

### Technical Improvements
- Migration to Python 3.x
- Containerized deployment (Docker)
- Cloud database integration
- Automated CI/CD pipeline
- Comprehensive API documentation (Swagger)
- Performance monitoring and analytics

## License

This project is available for educational and research purposes. Please ensure compliance with data scraping policies and terms of service for external platforms.

---

**Contact**: For questions about this machine learning platform, please refer to the project documentation or create an issue in the repository.

**Last Updated**: September 2025
