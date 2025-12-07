import LoginPanel from "./components/Login/Login"
import { Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import Register from "./components/Register";
import Dealers from "./components/Dealers";
import DealerDetails from "./components/DealerDetails";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/" element={<Home />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dealers" element={<Dealers />} />
      <Route path="/dealer/:id" element={<DealerDetails />} />
    </Routes>
  );
}
export default App;
