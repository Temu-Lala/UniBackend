

# University Social Media Platform

Welcome to the University Social Media Platform! This repository contains the source code for a real-time social media application designed for university communities. The platform includes features such as a chatting system, news posts, notifications, promotions, and hierarchical organization of university entities.

## Features

- **Real-Time Chatting System**: Instant messaging between users using Socket.IO.
- **News Post System**: Users can create, like, comment, and share posts.
- **Notifications**: Real-time notifications for various activities on the platform.
- **Promotions**: Mechanism for promoting events and announcements.
- **University Hierarchy**: Detailed organizational structure including campus, college, department, lectures, laboratories, and libraries.
- **Profiles & Ratings**: Users can view profiles of university entities and provide ratings.
- **Search Functionality**: Advanced search algorithm to find university profiles, departments, and more.
- **Mobile App**: Mobile application counterpart for seamless user experience.

## Tech Stack

### Frontend
- **React**
- **Next.js**
- **Tailwind CSS**
- **Ant Design**

### Backend
- **Python**
- **Django**
- **Django REST Framework**
- **Socket.IO**

### Mobile App
- Built using the same technology stack, optimized for mobile devices.

## Getting Started

### Prerequisites

- Node.js
- Python 3.x
- Django
- npm/yarn

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/university-social-media-platform.git
    cd university-social-media-platform
    ```

2. **Frontend Setup:**

    Navigate to the `frontend` directory and install dependencies:
    ```sh
    cd frontend
    npm install
    # or
    yarn install
    ```

    Start the development server:
    ```sh
    npm run dev
    # or
    yarn dev
    ```

3. **Backend Setup:**

    Navigate to the `backend` directory, create a virtual environment, and install dependencies:
    ```sh
    cd ../backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

    Run database migrations and start the Django server:
    ```sh
    python manage.py migrate
    python manage.py runserver
    ```

4. **Socket.IO Setup:**

    Make sure the Socket.IO server is running for real-time features:
    ```sh
    cd ../socket
    npm install
    npm start
    ```

### Mobile App Setup

For the mobile app setup, refer to the `mobile` directory and follow the instructions in the `README.md` file located there.

## Usage

- Register and log in to create a user account.
- Explore university entities and their profiles.
- Engage with news posts by liking, commenting, and sharing.
- Use the real-time chat feature to communicate with other users.
- Receive notifications for various activities.
- Rate and follow/unfollow university entities.

## Contributing

We welcome contributions! Please fork the repository and create a pull request for any enhancements, bug fixes, or new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please reach out to us at [temesgendebebe1921@gmail.com].

---

