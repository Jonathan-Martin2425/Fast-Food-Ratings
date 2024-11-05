CREATE TABLE Brands(
  b_id int generated always as identity not null PRIMARY KEY,
  created_at timestamp with time zone null default now(),
  name text not null,
  service_type text not null
);

CREATE TABLE  Food(
  f_id int generated always as identity not null PRIMARY KEY,
  brand_id int not null,
  FOREIGN KEY (brand_id) REFERENCES Brands(b_id),
  created_at timestamp with time zone null default now(),
  name text not null
);

CREATE TABLE  Catagories(
  food_id int not null,
  FOREIGN KEY (food_id) REFERENCES food(f_id),
  brand_id int not null,
  FOREIGN KEY (brand_id) REFERENCES Brands(b_id),
  created_at timestamp with time zone null default now(),
  catagory text not null
);

CREATE TABLE  Locations(
  l_id int generated always as identity not null PRIMARY KEY,
  brand_id int not null,
  FOREIGN KEY (brand_id) REFERENCES Brands(b_id),
  created_at timestamp with time zone null default now(),
  address text not null
);

CREATE TABLE Hours(
  id int generated always as identity not null PRIMARY KEY,
  created_at timestamp with time zone null default now(),
  business_id int not null,
  FOREIGN KEY (business_id) REFERENCES locations(l_id),
  day_of_week text not null,
  hours text not null
);

CREATE TABLE Users(
  u_id int generated always as identity not null PRIMARY KEY,
  created_at timestamp with time zone null default now(),
  name text not null
);

CREATE TABLE  Reviews(
  r_id int generated always as identity not null PRIMARY KEY,
  location_id int not null,
  FOREIGN KEY (location_id) REFERENCES Locations(l_id),
  date_published timestamp with time zone null default now(),
  publisher_id int not null REFERENCES Users(u_id),
  service_rating int not null,
  quality_rating int not null,
  cleanliness_rating int not null,
  description text not null
);

CREATE TABLE visited(
  v_id int generated always as identity not null PRIMARY KEY,
  created_at timestamp with time zone null default now(),
  user_id int not null,
  FOREIGN KEY (user_id) REFERENCES users(u_id),
  visit text not null
);


-- This is where a set of default values will be initialized
-- like McDonalds and the location on maddona rd
-- every table has at least 1 starting value, including reviews

INSERT INTO brands (name, service_type)
VALUES ('McDonalds', 'Fast Food');

INSERT INTO brands (name, service_type)
VALUES ('Del Taco', 'Fast Food');

INSERT INTO food (brand_id, name)
VALUES (1, 'Big Mac');

INSERT INTO catagories (brand_id, food_id, catagory)
VALUES (1, 1, 'Burger');

INSERT INTO locations (brand_id, address)
VALUES (1,  '275 Madonna Rd, San Luis Obispo, CA 93401');

INSERT INTO locations (brand_id, address)
VALUES (1,  '123 Bob Dr, Tustin, CA 92780');

INSERT INTO locations (brand_id, address)
VALUES (2,  '13742 Red Hill Ave, Tustin, CA 92780');

INSERT INTO Hours (business_id, day_of_week, hours)
VALUES (1, 'Monday', 'Open 24 Hours'),
(1, 'Tuesday', 'Open 24 Hours'),
(1, 'Wednesday', 'Open 24 Hours'),
(1, 'Thursday', 'Open 24 Hours'),
(1, 'Friday', 'Open 24 Hours'),
(1, 'Saturday', 'Open 24 Hours'),
(1, 'Sunday', 'Open 24 Hours'),
(2, 'Monday', 'Open 24 Hours'),
(2, 'Tuesday', 'Open 24 Hours'),
(2, 'Wednesday', 'Open 24 Hours'),
(2, 'Thursday', 'Open 24 Hours'),
(2, 'Friday', 'Open 24 Hours'),
(2, 'Saturday', 'Open 24 Hours'),
(2, 'Sunday', 'Open 24 Hours');

INSERT INTO users (name)
VALUES ('Anonymous');

INSERT INTO reviews(location_id, publisher_id, 
service_rating, quality_rating, cleanliness_rating, description)
VALUES (1, 1, 0, 0, 0, 'Complete garbage, will never go here again');

INSERT INTO visited (user_id, visit)
VALUES (1, 'McDonalds, 275 Madonna Rd, San Luis Obispo, CA 93401');
