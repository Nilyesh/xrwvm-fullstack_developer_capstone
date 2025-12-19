const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const  cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const port = 3031;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));
app.use(bodyParser.json());

const path = require('path');
const reviews_data = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'reviews.json'), 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'dealerships.json'), 'utf8'));

mongoose.connect("mongodb://localhost:27017/",{'dbName':'dealershipsDB'});


const Reviews = require('./review');
const Dealerships = require('./dealership');

// --- FIX: Safely determine the array of dealership objects ---
// Try to access the array using known names, falling back to an empty array
const rawDealershipsArray = 
    dealerships_data.dealerships || 
    dealerships_data.Dealerships || // Try capitalized D
    dealerships_data ||              // Try if it's a raw array at the root
    [];                             // Fallback to empty array

// 1. Map Dealerships Data to satisfy Mongoose Schema requirements (st -> state, Number -> String)
const mappedDealerships = Array.isArray(rawDealershipsArray) ? rawDealershipsArray.map(dealer => ({
    id: dealer.id,
    city: dealer.city,
    state: dealer.st,             // Mapped from JSON key 'st'
    address: dealer.address,
    zip: dealer.zip,
    lat: String(dealer.lat),
    long: String(dealer.long),
    full_name: dealer.full_name,
    short_name: dealer.short_name,
})) : [];


// 2. Reviews data: assume nested key based on your sample
const rawReviews = reviews_data['reviews'] || []; 

// 3. Database Seeding Logic
(async () => {
    try {
        await Reviews.deleteMany({});
        await Reviews.insertMany(rawReviews);

        await Dealerships.deleteMany({});
        await Dealerships.insertMany(mappedDealerships);

        console.log("Database seeded successfully");
    } catch (error) {
        console.error("Error seeding database:", error);
    }
})();


// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API")
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
    try {
        const documents = await Reviews.find({ dealership: req.params.id });
        res.json(documents);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching reviews' });
    }
});

// server/database/app.js

app.get('/fetchDealer/:id', async (req, res) => {
    try {
        const dealerId = parseInt(req.params.id); // Convert "7" to a number
        const dealer = await Dealerships.findOne({ id: dealerId }); // Use findOne for a single object
        
        if (dealer) {
            res.json(dealer);
        } else {
            res.status(404).json({ error: 'Dealer not found' });
        }
    } catch (error) {
        res.status(500).json({ error: 'Error fetching dealer' });
    }
});

// Express route to fetch all dealerships
// In your Node.js app.js
app.get('/fetchDealers', async (req, res) => {
    try {
        const documents = await Dealerships.find();
        res.json(documents);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching dealerships' });
    }
});

// Express route to fetch Dealers by a particular state
    app.get('/fetchDealers/state/:state', async (req, res) => {    
    try {
        const dealers = await Dealerships.find({ state: req.params.state });
        res.json(dealers);
      } catch (error) {
        res.status(500).json({ error: 'Error fetching dealers by state' });
      }
    });

// Express route to fetch dealer by a particular id
   
//Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
    try {
        const data = JSON.parse(req.body.toString());
        // Sort by id descending to get the highest one
        const documents = await Reviews.find().sort({ id: -1 }).limit(1);
        let new_id = (documents.length > 0) ? documents[0].id + 1 : 1;

        const review = new Reviews({
            "id": new_id,
            "name": data['name'],
            "dealership": data['dealership'],
            "review": data['review'],
            "purchase": data['purchase'],
            "purchase_date": data['purchase_date'],
            "car_make": data['car_make'],
            "car_model": data['car_model'],
            "car_year": data['car_year'],
        });

        const savedReview = await review.save();
        res.status(200).json(savedReview);
    } catch (error) {
        console.error("Node.js Error:", error);
        res.status(500).json({ error: 'Error inserting review' });
    }
});

// Start the Express server
app.listen(3031, () => {
    console.log('Express server started on port 3031');
});
