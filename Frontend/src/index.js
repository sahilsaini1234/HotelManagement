import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route,Routes } from 'react-router-dom';
import BookingList from './list';
import BookingForm from './App';
import './index.css';

ReactDOM.render( 
  <BrowserRouter>
  <Routes>
      <Route path="/" element={<BookingForm/>}/>
      <Route path="/bookings/edit/:bookingId" element={<BookingForm/>}/>
      <Route path="/view" element={<BookingList/>}/>
  </Routes> 
</BrowserRouter>
  ,
       document.getElementById('root')
);