# Trois
A card matching game made in ReactJS, where the differences are what matter.

# About This Project
I set out to replicate a game that my wife, friends and I enjoy, called [Set](https://www.playmonster.com/product/set/).

I changed around the symbols and threw in online connectivity so that we could all play together if we were missing a Set deck (or play solo if anyone preferred).

The goals of this project were simple:
1. Experiment with a React frontend; and
2. Experiment with alternative websocket and web server technologies in Python on the backend.

## How to play
In the game of Trois, there are many groups of three. There are three different shapes, which come in three different counts, and can have three different fillings, and three different colours. Your goal is to match all but one feature, or to match none of the features, of three cards. Trois is the French word for "three".

1. Draw 12 cards from the deck and place them face up in 3 rows of 4.
2. Look for groups of three cards that have all but one feature matching. Example:

  Card 1: 3 Purple Filled Triangles
  Card 2: 3 Purple Filled Squares
  Card 3: 3 Purple Filled Circles

## Dependencies
1. Python (https://www.python.org/)
2. Poetry (https://python-poetry.org/)
3. npm (https://www.npmjs.com/)

## Installing
1. Clone the repo.

### Client:
2. Navigate into the client directory.
3. `npm install`
4. `npm run build`

### Server:
5. Navigate into the server directory.
6. `poetry install`
7. `poetry run trois`
8. Server should be running at `localhost:8080`

## Tests
Frontend tests using Jest (https://jestjs.io/)

Run: `npm test`

Backend tests using Pytest (https://docs.pytest.org/en/7.1.x/)

Run: `poetry run pytest`