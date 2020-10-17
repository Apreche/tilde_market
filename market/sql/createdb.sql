-- All players in the game
CREATE TABLE players (
    name TEXT PRIMARY KEY NOT NULL,
    cash REAL DEFAULT 1000.00 NOT NULL CHECK(cash >= 0)
);

-- All publicly traded companies
CREATE TABLE companies (
    symbol TEXT PRIMARY KEY NOT NULL CHECK(length(symbol) <= 5),
    full_name TEXT UNIQUE NOT NULL,
    creator TEXT REFERENCES players UNIQUE NOT NULL
);
CREATE INDEX companycreatoridx ON companies(creator);

-- Track who owns all company shares
CREATE TABLE shares (
    company TEXT REFERENCES companies NOT NULL,
    player TEXT REFERENCES players NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity >= 0),
    UNIQUE(company, player)
);
CREATE INDEX sharecompanyidx ON shares(company);
CREATE INDEX shareplayeridx ON shares(player);

-- Track all data for each trading session
CREATE TABLE trading_sessions (
    id INTEGER PRIMARY KEY NOT NULL,
    datetime TEXT NOT NULL
);

-- Track every successfully submitted order
CREATE TABLE orders (
    orderid INTEGER PRIMARY KEY NOT NULL,
    session INTEGER REFERENCES trading_sessions NOT NULL,
    player TEXT REFERENCES players NOT NULL,
    company TEXT REFERENCES companies NOT NULL,
    type INTEGER NOT NULL CHECK(type >= 0 AND type <= 1), -- 0 = buy, 1 = sell
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    price REAL NOT NULL CHECK(price >= 0),
    UNIQUE(company, player)
);
CREATE INDEX ordersessionidx ON orders(session);
CREATE INDEX orderplayeridx ON orders(player);
CREATE INDEX ordercompanyidx ON orders(company);

-- If shares are exchanged, track it
CREATE TABLE trades (
    tradeid INTEGER PRIMARY KEY NOT NULL,
    buyorder REFERENCES orders NOT NULL,
    sellorder REFERENCES orders NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0)
);
CREATE INDEX tradebuyorderidx ON trades(buyorder);
CREATE INDEX tradesellorderidx ON trades(sellorder);
