# Gephyr

Gephyr is a small application that allows you to import AWS usage data from a parquet file and query it using a web interface or REST API.

## Setup

Prerequisites:

- Python 3.12+ (NOTE: earlier versions of Python 3 may work, but have not been tested)
- pip
- a parquet file containing usage data

Install the dependencies:

```
pip install -r requirements.txt
```

Create a .env file with the path to your parquet file and desired database path. You can start by copying the .env.example file, but make sure the path to your parquet file is correct.

```
cp .env.example .env
```

## Usage

### Loading Data

To load data into the database, run the following command:

```
python load_data.py
```

This will load the parquet file at the path specified in the .env file into the database at the path specified in the .env file.

### Running the Application

To run the application with the flask development server, run the following command: (Be sure to load data into the database first)

```
flask run
```

## API Endpoints

### GET /api/cost

Get the cost of a product by product_servicecode.
Setting the `use_discount` query parameter to `'true'` will apply the discount percentage specified in the discounts.json file for that product.

### GET /api/blended

Get the blended rate for all usage.

## Web Interface

The web interface is a simple form that allows you to enter a product service code and choose whether or not to apply a discount.
It will then display the total usage cost of the selected product.

It also includes a button to calculate the blended rate for all usage.

![screenshot of web interface](web-interface.png)

## Points of Discussion

### Assumptions

- The main overreaching assumption that I made was that this application is in no way meant to be production-ready. The instructions did not explicitly state this, but I think it's a reasonable assumption to make given the context and time expectation.
- I also assumed that we didn't need to load non-usage entries into the database, given that we wouldn't have been doing anything with them. A real application with more functionality might need all of the data in the parquet file.

### Takeaways and Things I'd Do Differently

- There isn't really anything major that I would do differently. I do wish that the frontend was a bit more polished as I don't think it shows off my skills there, but the instructions were pretty clear that it wasn't necessary.

### Production Considerations

There are a LOT of things that would need to be done differently to make this a production-ready application. Some would depend on existing infrastructure and/or architecture, while others would be specific to this application.

#### Database and Data Schema

- I'd never used DuckDB before, but it was very easy to get started with and specifcally made it easy to load data from a parquet file. I'm not sure if it would make sense for storing other data like users, customers, discounts, etc. in a production environment, but it worked well enough for my purposes in this application.

- Presumably this application would be used by multiple customers, so we'd need to at the very least identify which customer each usage record and discount records belong to, and which customer is currently using the application. We might want to go further and provide additional safeguards to ensure that usage records are separated by customer.

#### API

- We would absolutely need to require authentication to use the API, so that only authorized users can access data. This could be done using JWTs, sessions, SSO, or some other mechanism.

#### Web Interface

- The existing web interface is very rudimentary and could use some basic improvements in just about every way. Since it's an enterprise application, it doesn't need to be super fancy, but it could look more professional and modern.

- The current layout with the per-service query form and blended rate button right next to each other with no additional context isn't very intuitive. It's not clear what either piece of functionality does, or why they're there. We would definitely want to add some additional context to the page to make it easier to understand and use.

- Something as simple as a dropdown menu to select the product service code would be much more intuitive than a text input field.

#### Edge Cases and Error Handling

- The current error handling is very basic and could use some improvements. For example, we should probably return specific error codes and messages from the API for expected error cases, and display them in a more user-friendly way in the web interface.

- I didn't really handle any edge cases directly, opting for simple and hopefully reasonable defaults instead. For example, if the user asks for a discount for a product that doesn't have one, we return a default of 100%. This is probably fine for this application, but it's worth thinking about how to handle edge cases in a more robust way. I could definitely see users wanting feedback if they select discounted usage for a product that doesn't have a discount available.

#### Overall Architecture

- I opted to create a single service for both the API and the web interface because the code was going to be colocated anyways. In a production environment, it would probably make sense to split them into separate services.

#### Security Considerations

- We would absolutely need to require authentication to use the API, so that only authorized users can access data.
- We would also need to consider how to handle authentication and authorization for the web interface.
- I didn't implement CORS, CSP, or other basic security measures. They're not relevant when running the application locally, but would be necessary in a production environment.
- I also didn't do anything to sanitize user input, so the application could be vulnerable to SQL injection attacks if the user input is not properly sanitized.
-

#### Testing

- For a production application, I would want to write some automated tests for the API and web interface. I don't generally like to go overboard with testing, but I think it's important to have some basic unit and integration tests in place to make sure everything is working as expected.
- For this application, I would want to write some basic unit tests for the functions that calculate the cost and blended rate and integration tests for the API and potentially the web interface.

#### Deployment

- Deployment would most likely depend on the existing infrastructure. It could be containerized and deployed to a kubernetes cluste or similar infrastructure like AWS Fargate or ECS, or deployed to a more traditional environment like EC2 with a WSGI server like Gunicorn.
- If I were deploying it myself independently of any existing infrastructure I'd probably just use a hosted service like Elastic Beanstalk, Fly.io, or Render

#### Observability, etc.

- In a production environment, we would need to monitor the application for performance, availability, and other metrics.
- We would also need to consider how to handle errors and exceptions, and how to log them for debugging purposes.
- We would need to set up alerts for when certain thresholds are exceeded, and we would need to have some way to view and analyze the data to make sense of the alerts.

### Working with a Larger Dataset

- For a dataset on the order of 100x the one used there would need to be some additional considerations, but I don't think it would be too difficult to handle or require major changes to the application
- Loading the data into DuckDb would take longer, but I don' think that's particularly problematic. With the existing dataset it was near-instant, and given the way the application works it would be fine if it took a few minutes. In a production app we might want to have the data loading happen in a background job. I don't think there's any expectation that it should be instant.
- We'd probably want to cache the results of common queries, like the blended rate, so that we don't have to recalculate them every time. We could even calculate it when usage data is updated instead of when it's requested, if the calculation ends up being too expensive.

## Meta Questions

- This project took me around 6 or 7 hours to complete (including the time to write the README). I didn't specifically track the amount of time I spent on each step, but I think the breakdown is roughly as follows:

  - Understanding the challenge and researching possible tools and approaches - 1 hour
  - Setting up the project - a few minutes
  - Setting up the database and loading data - 1 hour
  - Writing the API and backend business logic - 1.5 hours
  - Building the web interface - 30 minutes
  - Testing, iterating, debugging, improving - 1 hour
  - Writing the README - 1 hour

- I have worked with Python and Flask a lot in the past, but it's been a few years since I used them on a daily basis.
- I've never used DuckDB or Parquet files before, so I had to do a little research to learn about them. I did also look into using Clickhouse. I chose DuckDB because it seemed easier to get started with for a small project like this.
- The instructions for the project were quite detailed and clear for the most part. It confused me a bit that the blended rate would be grouped with the per-service costs, but that's more of a user experience issue for the application than an issue with the instructions. I think in the context of a larger application with more other features, it would probably be fine. Additional guidance for the frontend portion might be helpful, though.
