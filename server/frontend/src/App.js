import { Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import LoginPanel from "./components/Login/Login"
import Register from "./components/Register/Register";
import Dealer from "./components/Dealers/Dealer";
import DealerDetails from "./components/DealerDetails";
import PostReview from "./components/Dealers/PostReview";


function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dealers" element={<Dealer />} />
      <Route path="/dealer/:id" element={<DealerDetails />} />
      <Route path="/postreview/:id" element={<PostReview />} />
  </Routes>
  );
}
export default App;
