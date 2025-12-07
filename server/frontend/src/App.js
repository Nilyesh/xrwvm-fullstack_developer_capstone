import LoginPanel from "./components/Login/Login"
import { Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import Register from "./components/Register";
import Dealers from "./components/Dealers/Dealer";
import DealerDetails from "./components/DealerDetails";
import PostReview from "./components/Dealers/PostReview";


function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/" element={<Home />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dealers" element={<Dealer/>} />
      <Route path="/dealer/:id" element={<DealerDetails />} />
      <Route path="/postreview/:id" element={<PostReview />} />
  </Routes>
  );
}
export default App;
