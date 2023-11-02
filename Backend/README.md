# Hotel Booking Backend

Welcome to the Hotel Booking Backend! This Flask-based backend provides APIs to manage hotel room bookings, including creating, editing, and canceling bookings. It also allows you to view bookings based on various criteria such as room type, user email, and date range.


## Introduction

The Hotel Booking Backend is designed to serve as the server-side component of a hotel room booking system. It includes the following features:

- Creating new bookings
- Editing existing bookings
- Canceling bookings
- Viewing bookings based on room type, user email, and date range

This README provides an overview of the project, instructions for setting up and running the backend, and an explanation of the available API endpoints.

## Features

- **Create Booking**: Allows users to create new bookings, specifying user email, room number, start time, and end time.

- **Edit Booking**: Supports the editing of existing bookings, including user email, start time, end time, and room number.

- **Cancel Booking**: Enables users to cancel their bookings, with refund calculations based on the time of cancellation.

- **View Bookings**: Provides endpoints for viewing bookings based on different criteria, including room type, user email, and date range.

## Prerequisites

Before getting started, ensure you have the following prerequisites:

- Python 3.x
- Flask
- SQLAlchemy
- MySQL database (or the database of your choice)
- Flask-CORS
- Flask-MySQLdb

You can install these dependencies using `pip`.

## Getting Started

1. Clone this repository to your local machine.
2. Install the required Python packages by running:


3. Create a MySQL database and update the `SQLALCHEMY_DATABASE_URI` configuration in `app.py` with your database connection details.

4. Run the backend server by executing:


The backend should now be running locally on `http://localhost:5000`.

## API Endpoints

The Hotel Booking Backend provides the following API endpoints:

- **Create Booking**: POST `/bookings/create`
- **Edit Booking**: PUT `/bookings/edit/<booking_id>`
- **Cancel Booking**: DELETE `/bookings/cancel/<booking_id>`
- **View Bookings**: GET `/bookings/view`



Assumptions

# 3 Types of Rooms are there  (A,B,C)
# A=500 
# B=200
# C=100
# ONLY ADMIN VIEW IS CREATED

