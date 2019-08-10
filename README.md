# food-delivery

__food-delivery__ is an API for food delivery platforms. The project aims to efficiently manage the process of food delivery among the store managers and the delivery agents. See the API docs [here](#api-documentation)

## Getting Started

### How to run locally

Clone the repository
```sh
$ git clone https://github.com/ashwani99/food-delivery
$ cd food-delivery
```

Create a virtual environment(optional but recommended) and install the dependencies
```sh
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt # dependency installing step
```

Setup your app's environment variables
```sh
(venv) $ export FOOD_DELIVERY_SECRET='this-no-one-can-guess'
(venv) $ export FLASK_APP=food-delivery/api.py
(venv) $ export DATABASE_URL=sqlite:///food.db
(venv) $ export FLASK_DEBUG=1 # optional if debug mode not needed
```

Initiate database
```sh
(venv) $ python food-delivery/init_db.py 
```

Run the API server
```sh
(venv) $ flask run --port 8080
```

## API documentation
### Overview
- [Authentication](#authentication)
- [Errors](#erros)

#### Authentication
The authentication system uses JWT token to authenticate system. So on the client has to provide the `access token` with each every request that requires authentication. Requests that require authentication will return `401 Unauthorized` if not authenticated.

`POST /login`
```json
{
	"email": "john@cena.com",
	"password": "johncena"
}
```

On successful credentials processing, the server will return a `JWT` Bearer token. Users need to add the authentication header `Authentication: Bearer <access-token>` with further requests that require authentication/authorization.

```json
{
    "access_token": "<your-access-token>"
}
```

#### Errors


### Core Resources
- [User list](#user-list)
- [User resource](#user-resource)
- [Delivery task list](#delivery-task-list)
- [Delivery task detail](#delivery-task-detail)
- [Change delivery task state](#change-delivery-task-state)

#### User list
##### Create a new user
Registers a new user

`POST /users`

__Parameters__

Name | Type | Description
---|---|---
`name` | `string` | __Required.__ Full name of the user
`email` | `string` | __Required.__ Email of the user
`password` | `string` | __Required.__ User's password

__Example input__

```json
{
    "name": "John Doe",
    "email": "john_doe@example.com",
    "password": "johndoe"
}
```

__Example response__

`201 Created`
```json
{
    "id": 6,
    "name": "John Doe",
    "email": "john_doe@example.com"
}
```

##### List all users
Get a list of all users

`GET /users`

__Example response__
`200 OK`
```json
[
    {
        "id": 1,
        "name": "John Sena",
        "email": "john@cena.com"
    },
    {
        "id": 2,
        "name": "Agent Vinod",
        "email": "agent@vinod.com"
    },
    {
        "id": 3,
        "name": "Tony Stark",
        "email": "tony@stark.com"
    },
    {
        "id": 4,
        "name": "Flash Superhero",
        "email": "flash@superhero.com"
    },
    {
        "id": 5,
        "name": "Spider Man",
        "email": "spider@man.com"
    },
    {
        "id": 6,
        "name": "John Doe",
        "email": "john_doe@example.com"
    }
]
```

#### User resource
##### Get an user resource
Get a particular user resource

`GET /user/:id`

__Example response__

`200 OK`
```json
{
    "id": 6,
    "name": "John Doe",
    "email": "john_doe@example.com"
}
```

##### Update an user resource
Update a particular user resource. The input should be a user JSON object.

`PUT /user/:id`

__Parameters__

Name | Type | Description
---|---|---
`name` | `string` | __Required.__ Full name of the user
`email` | `string` | __Required.__ Email of the user
`password` | `string` | __Required.__ User's password

__Example input__

`PUT /user/6`
```json
{
    "id": 6,
    "name": "John Doe Reloaded",
    "email": "john_doe@example.com",
    "password": "newpassword"
}
```

__Example response__

`200 OK`
```json
{
    "email": "john_doe@example.com",
    "id": 6,
    "name": "John Doe Reloaded"
}
```

##### Delete an user resource
Deletes a particular user resource from the server.

`DELETE /user/:id`

Returns a `204 No Content` if successful

#### Delivery task list
##### Get all tasks
Get all tasks created or assigned to the authenticated user.

For store managers: returns all tasks created by the store manager

For delivery agents: returns all tasks accepted by the delivery agent

`GET /tasks`

__Example response__

`200 OK`
```json
[
    {
        "destination": "Down Town",
        "last_updated_at": "2019-08-09T08:22:51.288927+00:00",
        "priority": "medium",
        "created_by": 1,
        "title": "Hot Chicken Kathi Roll",
        "created_at": "2019-08-09T08:22:51.288923+00:00",
        "accepted_by": 2,
        "current_state": "not implemented",
        "id": 1
    },
    {
        "destination": "Home",
        "last_updated_at": "2019-08-09T08:22:51.289296+00:00",
        "priority": "high",
        "created_by": 1,
        "title": "Mutton Biryani",
        "created_at": "2019-08-09T08:22:51.289294+00:00",
        "accepted_by": null,
        "current_state": "not implemented",
        "id": 2
    }
]
```

##### Create a new task
Creates a new task for for authenticated store manager

`POST /tasks`

__Parameters__

Name | Type | Description
---|---|---
`title` | `string` | __Required.__ Name of the delivery task
`priority` | `string` | __Required.__ Priority of the delivery task. It should be one of among `low`, `medium` and `high`
`destination` | `string` | __Required.__ Destination where the food will be delivered

__Example input__
```json
{
	"title": "Phirni",
	"priority": "high",
	"destination": "office"
}
```

__Example response__

`201 Created`
```json
{
    "states": [
        {
            "updated_at": "2019-08-10T09:24:47.124650+00:00",
            "state": "new"
        }
    ],
    "destination": "office",
    "last_updated_at": "2019-08-10T09:24:47.122613+00:00",
    "priority": "high",
    "created_by": 1,
    "title": "Phirni",
    "created_at": "2019-08-10T09:24:47.122607+00:00",
    "accepted_by": null,
    "current_state": "not implemented",
    "id": 4
}
```

#### Delivery task detail
##### Get delivery task details
Gets details of a particular delivery task

`GET /task/:id`

__Example response__
`200 OK`
```json
{
    "states": [
        {
            "updated_at": "2019-08-10T09:24:47.124650+00:00",
            "state": "new"
        }
    ],
    "destination": "office",
    "last_updated_at": "2019-08-10T09:24:47.122613+00:00",
    "priority": "high",
    "created_by": 1,
    "title": "Phirni",
    "created_at": "2019-08-10T09:24:47.122607+00:00",
    "accepted_by": null,
    "current_state": "not implemented",
    "id": 4
}
```

##### Update delivery task
Updates a particular task

`PUT /task/:id`

__Parameters__

Name | Type | Description
---|---|---
`title` | `string` | __Required.__ Name of the delivery task
`priority` | `string` | __Required.__ Priority of the delivery task. It should be one of among `low`, `medium` and `high`
`destination` | `string` | __Required.__ Destination where the food will be delivered

__Example input__
`PUT /task/2`
```json
{
	"title": "Phirni",
	"priority": "high",
	"destination": "office"
}
```

__Example response__

`200 OK`
```json
{
    "states": [
        {
            "updated_at": "2019-08-09T08:22:51.290782+00:00",
            "state": "new"
        }
    ],
    "current_state": "not implemented",
    "last_updated_at": "2019-08-10T12:24:14.989757+00:00",
    "priority": "high",
    "title": "Mutton Biryani",
    "created_at": "2019-08-09T08:22:51.289294+00:00",
    "id": 2,
    "accepted_by": null,
    "destination": "office2",
    "created_by": 1
}
```

##### Cancel a delivery task
Cancels the delivery task

`DELETE /task/:id`

__Example response__

`DELETE /task/2`

`200 OK`
```json
{
    "msg": "Successfully cancelled task"
}
```

#### Change delivery task state
Changes the state of the delivery task. States can be one of among `new`, `accepted`, `complete`, `decline`, `cancel`

__Example response__

`POST /task/4/cancel`
```json
{
    "msg": "Success!"
}
```

### User roles


