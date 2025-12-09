CREATE TABLE park (
    id TEXT PRIMARY KEY,
    fullName TEXT NOT NULL,
    parkCode TEXT NOT NULL,
    description TEXT NOT NULL,
    latitude TEXT NOT NULL,
    longitude TEXT NOT NULL,
    latLong TEXT NOT NULL,
    states TEXT NOT NULL,
    directionsInfo TEXT NOT NULL,
    name TEXT NOT NULL,
    designation TEXT NOT NULL
);

CREATE TABLE visitorcenter (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    parkCode TEXT NOT NULL,
    description TEXT NOT NULL,
    latitude TEXT NOT NULL,
    longitude TEXT NOT NULL,
    directionsInfo TEXT NOT NULL,
    park_id TEXT,
    FOREIGN KEY (park_id) REFERENCES park (id)
);

CREATE TABLE activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nps_id TEXT NOT NULL,
    name TEXT NOT NULL,
    park_id TEXT,
    FOREIGN KEY (park_id) REFERENCES park (id)
);
