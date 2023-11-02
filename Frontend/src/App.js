import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './App.css'
import { Link } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
  
const notify = () => toast("Booked room succesfully!")
const edited = () => toast("Edited room succesfully!")
const invalid = () => toast("Invalid room id or Booking overlaped")
const swr = () => toast("Something went wrong!")
function BookingForm() {
  const { bookingId } = useParams();
  const [formData, setFormData] = useState({
    user_email: '',
    room_number: '',
    start_time: '',
    end_time: '',
  });


  const handleSubmit = (e) => {
    e.preventDefault();

    if (bookingId) {
      fetch(`http://127.0.0.1:5000/bookings/edit/${bookingId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })
        .then((response) => {
          if (response.ok) {
            edited();
          }
          else{
            swr();
          }
        });
    } else {

      fetch('http://127.0.0.1:5000/bookings/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })
        .then((response) => {
          console.log(response)
          if (response.ok) {
            notify();
          }
          else{
             invalid();
          }
        });
    }
  };

  return (
    <div className="container">
      <h2>{bookingId ? 'Edit Booking' : 'Create Booking'}</h2>
      <form name="form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="User Email"
          name="user_email"
          value={formData.user_email}
          onChange={(e) => setFormData({ ...formData, user_email: e.target.value })}
        />
        <br />
        <input
          type="text"
          placeholder="Room Number"
          name="room_number"
          value={formData.room_number}
          onChange={(e) => setFormData({ ...formData, room_number: e.target.value })}
        />
        <br />
        <input
          type="datetime-local"
          placeholder="Start Time"
          name="start_time"
          value={formData.start_time}
          onChange={(e) => setFormData({ ...formData, start_time: e.target.value })}
        />
        <br />
        <input
          type="datetime-local"
          placeholder="End Time"
          name="end_time"
          value={formData.end_time}
          onChange={(e) => setFormData({ ...formData, end_time: e.target.value })}
        />
        <br /><br /><br />
        <button type="submit">{bookingId ? 'Save Changes' : 'Create Booking'}</button>
      </form>
      <ToastContainer/>
      <Link to="/view">Views</Link>
    </div>
  );
}

export default BookingForm;
