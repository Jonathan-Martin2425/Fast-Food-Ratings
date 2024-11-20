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

CREATE TABLE  Categories(
  food_id int not null,
  FOREIGN KEY (food_id) REFERENCES food(f_id),
  created_at timestamp with time zone null default now(),
  category text not null
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
VALUES ('McDonalds', 'Fast Food'),
('Del Taco', 'Fast Food'),
('Dominos', 'Pizza Delivery'),
('Five Guys', 'Fast Food');

INSERT INTO food (brand_id, name)
VALUES (1, 'Big Mac'),
(1, 'Fries'),
(2, 'The Del Taco'),
(2, 'Crinkle-Cut Fries'),
(3, 'Meat Lovers'),
(3, 'Pepperoni'),
(4, 'Single Cheeseburger'),
(4, 'Cajun Fries');

INSERT INTO categories (food_id, category)
VALUES (1, 'Burger'),
(2, 'Side'),
(3, 'Taco'),
(4, 'Side'),
(5, 'Pizza'),
(6, 'Pizza'),
(7, 'Burger'),
(8, 'Side');

INSERT INTO locations (brand_id, address)
VALUES (1,  '275 Madonna Rd, San Luis Obispo, CA 93401'),
(1,  '123 Bob Dr, Tustin, CA 92780'),
(2,  '13742 Red Hill Ave, Tustin, CA 92780'),
(3, '866 Foothill Blvd, San Luis Obispo, CA 93405'),
(4, '763 Foothill Blvd, San Luis Obispo, CA 93405'),
(1, '350 5 Cities Dr, Pismo Beach, CA 93449'),
(1, '1550 W Grand Ave, Grover Beach, CA 93433');


INSERT INTO Hours (business_id, day_of_week, hours)
VALUES (1, 'Monday', 'Open 24 Hours'),
(1, 'Tuesday', 'Open 24 Hours'),
(1, 'Wednesday', 'Open 24 Hours'),
(1, 'Thursday', 'Open 24 Hours'),
(1, 'Friday', 'Open 24 Hours'),
(1, 'Saturday', 'Open 24 Hours'),
(1, 'Sunday', 'Open 24 Hours'),
(2, 'Monday', '7am-10pm'),
(2, 'Tuesday', '7am-10pm'),
(2, 'Wednesday', '7am-10pm'),
(2, 'Thursday', '7am-10pm'),
(2, 'Friday', '7am-12am'),
(2, 'Saturday', '8am-2am'),
(2, 'Sunday', '8am-10pm'),
(3, 'Monday', 'Open 24 Hours'),
(3, 'Tuesday', 'Open 24 Hours'),
(3, 'Wednesday', 'Open 24 Hours'),
(3, 'Thursday', 'Open 24 Hours'),
(3, 'Friday', 'Open 24 Hours'),
(3, 'Saturday', 'Open 24 Hours'),
(3, 'Sunday', 'Open 24 Hours'),
(4, 'Monday', '11am-2am'),
(4, 'Tuesday', '11am-2am'),
(4, 'Wednesday', '11am-2am'),
(4, 'Thursday', '11am-2am'),
(4, 'Friday', '11am-2am'),
(4, 'Saturday', '11am-2am'),
(4, 'Sunday', '11am-2am'),
(5, 'Monday', '11am-10pm'),
(5, 'Tuesday', '11am-10pm'),
(5, 'Wednesday', '11am-10pm'),
(5, 'Thursday', '11am-10pm'),
(5, 'Friday', '11am-10pm'),
(5, 'Saturday', '11am-10pm'),
(5, 'Sunday', '11am-10pm');

INSERT INTO users (name)
VALUES ('Anonymous'),
('Karen Willoughby'),
('Randy Jr'),
('Meaty Marley'),
('Jonathan Martin'),
('Carlos Lopez'),
('Willeam Mendez'),
('Justin Timberlake'),
('The Creature'),
('Cassidy');

INSERT INTO reviews(location_id, publisher_id, 
service_rating, quality_rating, cleanliness_rating, description)
VALUES (1, 1, 0, 0, 0, 'Complete garbage, will never go here again'),
(4, 1, 10, 10, 10, 'Best Dominos Ever. took less than 10 min from ordering to get food, it was somehow better than other dominos I have gone too AND was spotless down to the area behind the drinks.');

INSERT INTO visited (user_id, visit)
VALUES (1, '275 Madonna Rd, San Luis Obispo, CA 93401'),
(1, '866 Foothill Blvd, San Luis Obispo, CA 93405');