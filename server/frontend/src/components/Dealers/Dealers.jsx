import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png";

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);

  const dealer_url = "/djangoapp/get_dealers/";

 useEffect(() => {
    const get_dealers = async () => {
      try {
        const res = await fetch(dealer_url, { method: "GET" });
        const retobj = await res.json();
        
        console.log("Data received from backend:", retobj);

        // Check if retobj itself is the array OR if it's inside retobj.dealers
        // Also handle cases where status might be a string "200" or a number 200
        if (retobj.status == 200 || Array.isArray(retobj)) {
          const all_dealers = Array.isArray(retobj) ? retobj : (retobj.dealers || []);
          
          if (all_dealers.length > 0) {
            const uniqueStates = [...new Set(all_dealers.map(dealer => dealer.state))].filter(Boolean);
            setStates(uniqueStates);
            setDealersList(all_dealers);
          } else {
            console.error("No dealers found in the response");
          }
        } else {
          console.error("Backend returned non-200 status:", retobj);
        }
      } catch (error) {
        console.error("Error fetching dealers:", error);
      }
    };

    get_dealers();
  }, []);
  // Filter dealers by state
  const filterDealers = async (state) => {
    try {
      const filtered_url = dealer_url + state; // e.g., /djangoapp/get_dealers/CA
      const res = await fetch(filtered_url, { method: "GET" });
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      const retobj = await res.json();
      if (retobj.status === 200) {
        const state_dealers = Array.from(retobj.dealers ?? []);
        setDealersList(state_dealers);
      } else {
        console.error("Failed to fetch filtered dealers:", retobj);
      }
    } catch (error) {
      console.error("Error fetching filtered dealers:", error);
    }
  };

let isLoggedIn = sessionStorage.getItem("username") != null ? true : false;

return(  <div>
      <Header/>

     <table className='table'>
      <tr>
      <th>ID</th>
      <th>Dealer Name</th>
      <th>City</th>
      <th>Address</th>
      <th>Zip</th>
      <th>
      <select name="state" id="state" onChange={(e) => filterDealers(e.target.value)}>
      <option value="" selected disabled hidden>State</option>
      <option value="All">All States</option>
      {states.map(state => (
          <option value={state}>{state}</option>
      ))}
      </select>        

      </th>
      {isLoggedIn ? (
          <th>Review Dealer</th>
         ):<></>
      }
      </tr>
     {dealersList.map(dealer => (
        <tr>
          <td>{dealer['id']}</td>
          <td><a href={'/dealer_details/'+dealer['id']}>{dealer['full_name']}</a></td>
          <td>{dealer['city']}</td>
          <td>{dealer['address']}</td>
          <td>{dealer['zip']}</td>
          <td>{dealer['state']}</td>
          {isLoggedIn ? (
            <td><a href={`/postreview/${dealer['id']}`}><img src={review_icon} className="review_icon" alt="Post Review"/></a></td>
           ):<></>
          }
        </tr>
      ))}
     </table>;
  </div>
)
}

export default Dealers
