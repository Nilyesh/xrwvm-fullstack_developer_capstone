import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Header from '../Header/Header';
import "./Dealers.css";

// Importing assets correctly
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";

const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const { id } = useParams();

  /// Corrected URLs to match your specific urlpatterns
const dealer_url = `/djangoapp/dealer/${id}/`; 
const reviews_url = `/djangoapp/reviews/dealer/${id}/`;
const post_review_url = `/postreview/${id}/`;

  const get_dealer = async () => {
    const res = await fetch(dealer_url);
    const retobj = await res.json();
    if (retobj.status === 200) {
      setDealer(retobj.dealer);
    }
  };

  const get_reviews = async () => {
    const res = await fetch(reviews_url);
    const retobj = await res.json();
    if (retobj.status === 200) {
      if (retobj.reviews.length > 0) {
        setReviews(retobj.reviews);
      } else {
        setUnreviewed(true);
      }
    }
  };

  const senti_icon = (sentiment) => {
    if (sentiment === "positive") return positive_icon;
    if (sentiment === "negative") return negative_icon;
    return neutral_icon;
  };

  useEffect(() => {
    get_dealer();
    get_reviews();
// eslint-disable-next-line react-hooks/exhaustive-deps  
}, [id]);

  // Guard clause to prevent crash while loading
  if (!dealer || Object.keys(dealer).length === 0) {
    return (
        <div>
            <Header />
            <div className="container mt-5">
                <div className="alert alert-warning">
                    <strong>Status:</strong> Component loaded, but waiting for data for Dealer #{id}...
                </div>
            </div>
        </div>
    );
  }

  return (
    <div className="container" style={{ margin: "20px" }}>
      <Header />
      
      {/* Dealer Info Card */}
      <div className="card" style={{ marginTop: "20px", padding: "20px" }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h1 style={{ color: "black", margin: 0 }}>{dealer.full_name}</h1>
            
            {/* Link to Post Review with the Button Icon */}
            <a href={post_review_url}>
                <img 
                    src={review_icon} 
                    style={{ width: '50px', cursor: 'pointer' }} 
                    alt="Post Review" 
                />
            </a>
        </div>
        
        <p className="card-text" style={{ marginTop: '10px' }}>
          <strong>Location:</strong> {dealer.city}, {dealer.address}, Zip - {dealer.zip}, {dealer.state}
        </p>
      </div>
      
      {/* Reviews Section */}
      <div className="reviews_panel mt-4" style={{ display: 'flex', flexWrap: 'wrap', gap: '20px' }}>
        {reviews.length === 0 ? (
          <div className="alert alert-info">No reviews yet for this dealership.</div>
        ) : (
          reviews.map(review => (
            <div className='card' key={review.id} style={{ width: '18rem', padding: '10px' }}>
              <img 
                src={senti_icon(review.sentiment)} 
                className="emotion_icon" 
                alt='Sentiment' 
                style={{ width: '40px' }} 
              />
              <div className="card-body">
                <p className='card-text' style={{ fontStyle: 'italic' }}>"{review.review}"</p>
                <h5 className="card-title" style={{ fontSize: '1rem' }}>{review.name}</h5>
                <h6 className="card-subtitle mb-2 text-muted">
                  {review.car_make} {review.car_model}, {review.car_year}
                </h6>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Dealer;