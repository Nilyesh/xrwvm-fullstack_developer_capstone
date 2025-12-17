import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";
import Header from '../Header/Header';

const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const [postReview, setPostReview] = useState(<></>);

  const params = useParams();
  const id = params.id;
  const root_url = window.location.origin;
  
  const dealer_url = `${root_url}/djangoapp/dealer/${id}/`;
  const reviews_url = `${root_url}/djangoapp/reviews/dealer/${id}/`;
  const post_review_url = `${root_url}/postreview/${id}/`;

  const get_dealer = async () => {
    console.log("Fetching dealer from URL:", dealer_url);
    const res = await fetch(dealer_url);
    const retobj = await res.json();
    
    if (retobj.status === 200) {
      // If the backend returns a single object, use it directly. 
      // If it returns a list, take the first item.
      const data = Array.isArray(retobj.dealer) ? retobj.dealer[0] : retobj.dealer;
      setDealer(data);
    }
  };    

  const get_reviews = async () => {
    const res = await fetch(reviews_url);
    const retobj = await res.json();
    if (retobj.status === 200) {
      if (retobj.reviews && retobj.reviews.length > 0) {
        setReviews(retobj.reviews);
      } else {
        setUnreviewed(true);
      }
    }
  };

  const senti_icon = (sentiment) => {
    return sentiment === "positive" ? positive_icon : 
           sentiment === "negative" ? negative_icon : neutral_icon;
  };

  useEffect(() => {
    get_dealer();
    get_reviews();
    if (sessionStorage.getItem("username")) {
      // FIX: Changed post_review to post_review_url
      setPostReview(
            <a href={post_review_url}>
        <img src={review_icon} style={{width:'10%', marginLeft:'10px', marginTop:'10px'}} alt='Post Review'/>
        </a>
      );
    }
  }, [id]); // Watch for ID changes

  return (
    <div style={{margin:"20px"}}>
      <Header/>
      <div style={{marginTop:"10px"}}>
        <h1 style={{color:"grey"}}>{dealer.full_name}{postReview}</h1>
        <h4 style={{color:"grey"}}>
            {dealer.city}, {dealer.address}, Zip - {dealer.zip}, {dealer.state}
        </h4>
      </div>
      <div className="reviews_panel">
        {reviews.length === 0 && unreviewed === false ? (
          <p>Loading Reviews....</p>
        ) : unreviewed === true ? (
          <div>No reviews yet!</div>
        ) : (
          reviews.map(review => (
            <div className='review_panel' key={review.id}>
              <img src={senti_icon(review.sentiment)} className="emotion_icon" alt='Sentiment'/>
              <div className='review'>{review.review}</div>
              <div className="reviewer">
                {review.name} {review.car_make} {review.car_model} {review.car_year}
              </div>
            </div>
          ))
        )}
      </div>  
    </div>
  );
}

export default Dealer;
