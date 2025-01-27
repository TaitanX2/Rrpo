#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No color

echo -e "${GREEN}Starting VPS Installer for BanallRepo...${NC}"

# Update and install system dependencies
echo -e "${GREEN}Installing system dependencies...${NC}"
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-pip python3-virtualenv screen

# Clone the repository
if [ ! -d "BanallRepo" ]; then
    echo -e "${GREEN}Cloning the repository...${NC}"
    git clone https://github.com/stkeditz/BanallRepo.git
    cd BanallRepo || { echo -e "${RED}Failed to enter repository directory!${NC}"; exit 1; }
else
    echo -e "${RED}Repository already exists. Skipping cloning.${NC}"
    cd BanallRepo
fi

# Set up virtual environment
echo -e "${GREEN}Setting up Python virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m virtualenv venv
fi
source venv/bin/activate

# Install Python dependencies
echo -e "${GREEN}Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Set up environment variables
echo -e "${GREEN}Setting up environment variables...${NC}"
if [ ! -f ".env" ]; then
    read -p "Enter BOT_TOKEN: " BOT_TOKEN
    read -p "Enter API_ID: " API_ID
    read -p "Enter API_HASH: " API_HASH
    read -p "Enter OWNER_ID: " OWNER_ID

    echo "BOT_TOKEN=$BOT_TOKEN" > .env
    echo "API_ID=$API_ID" >> .env
    echo "API_HASH=$API_HASH" >> .env
    echo "OWNER_ID=$OWNER_ID" >> .env
    echo -e "${GREEN}Environment variables saved to .env file.${NC}"
else
    echo -e "${RED}.env file already exists. Skipping variable setup.${NC}"
fi

# Start the bot
echo -e "${GREEN}Starting the bot...${NC}"
screen -dmS banallbot bash -c "source venv/bin/activate && python3 bot.py"

echo -e "${GREEN}Bot started successfully in a screen session named 'banallbot'. Use 'screen -r banallbot' to view logs.${NC}"
