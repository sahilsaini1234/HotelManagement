import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './List.css';

const notify = () => toast("Deleted Booking successfully!");

function BookingList() {
  const [bookings, setBookings] = useState([]);
  const [filters, setFilters] = useState({
    room_type: '', // to store selected room type
    user_email: '', // to store entered user email
    start_time: '', // to store selected start date
    end_time: '',   // to store selected end date
  });

  const fetchData = async () => {
    const queryParams = new URLSearchParams(filters).toString();
    await fetch(`http://127.0.0.1:5000/bookings/view?${queryParams}`)
      .then((response) => response.json())
      .then((data) => setBookings(data.bookings));
  }

  useEffect(() => {
    fetchData();
  }, []);

  const handleChanges = () => {
    fetchData();
  }
  const handleClear = () => {
    setFilters({
      room_type: '',
      user_email: '',
      start_time: '', 
      end_time: '',  
    })
    fetchData();
  }

  const handleDelete = async (bookingId) => {
    await fetch(`http://127.0.0.1:5000/bookings/cancel/${bookingId}`, {
      method: 'DELETE',
    }).then((response)=>response.json())
    .then((data)=>{
      console.log(data)
      const refundAmount = data.refund_amount;
      const delete_notify = () => toast(`Your ${refundAmount} Will be refunded into your bank account`);
      delete_notify()
    }
    )
    .then(() => {
      const updatedBookings = bookings.filter((booking) => booking.id !== bookingId);
      setBookings(updatedBookings);  notify();

    })
  };


  const handleFilterChange = (event) => {
    const { name, value } = event.target;
    setFilters({ ...filters, [name]: value });
    console.log(filters);
  };

  return (
    <div>
      <h2>Booking List</h2>
      <div className="filter-options">
        <label>
          <input
            type="radio"
            name="room_type"
            value="A"
            checked={filters.room_type === 'A'}
            onChange={handleFilterChange}
          />
          Room Type A
        </label>
        <label>
          <input
            type="radio"
            name="room_type"
            value="B"
            checked={filters.room_type === 'B'}
            onChange={handleFilterChange}
          />
          Room Type B
        </label>
        <label>
          <input
            type="radio"
            name="room_type"
            value="C"
            checked={filters.room_type === 'C'}
            onChange={handleFilterChange}
          />
          Room Type C
        </label>
        <br />
        <input
          type="text"
          name="user_email"
          placeholder="User Email"
          value={filters.user_email}
          onChange={handleFilterChange}
        />
        <input
          type="date"
          name="start_time"
          value={filters.start_time}
          onChange={handleFilterChange}
        />
        <input
          type="date"
          name="end_time"
          value={filters.end_time}
          onChange={handleFilterChange}
        />
        <br /><br />
        <div className="filterapply">
        <button onClick={handleChanges}>
          Apply Filters
        </button>
        <button onClick={handleClear}>
          Clear
        </button>
        </div>
      </div>
      <ul>
        {bookings.map((booking) => (
          <li key={booking.id}>
            <div className="card">
              <p>User Email: {booking.user_email}</p>
              <p>Room_id: {booking.room_id}</p>
              <p>Room_type: {booking.room_type}</p>
              <p>Start_time: {booking.start_time}</p>
              <p>End_time: {booking.end_time}</p>
              <div className="Link">
                <Link to={`/bookings/edit/${booking.id}`}>Edit</Link>
                <button onClick={() => handleDelete(booking.id)}>Delete</button>
              </div>
            </div>
          </li>
        ))}
      </ul>
      <ToastContainer />
      <Link to="/">Create Booking</Link>
    </div>
  );
}

export default BookingList;
