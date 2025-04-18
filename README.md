# Final Project for DS 4300

By G. Mackin, Lauren Cummings, Rhea Kallely, Melina Lymberopoulos

This repository represents our team's submission for the final project for DS 4300. Please refer to our [slide deck](https://docs.google.com/presentation/d/1wYM0O5ZRoPSXxt2dlKo8H95-UUNLBpvNazrBzyEsS5U/edit?usp=sharing) for more on the details on our submission.

## Prerequisites

- RDS instance running using MySQL
- EC2 set up with this repository cloned onto it
- Renamed `src/.env.example` to `src/.env` and configured properly
- Ensure you have the key pair (`keypair.pem`) for EC2 downloaded
- Python 3 and required libraries installed on EC2
  - Run `pip install pymysql boto3 numpy pillow streamlit` in the terminal
- Lambda set up (read `src/lambda/README.md` for more)

## How to Run

1. SSH into the EC2 instance
    - `ssh -i path/to/keypair.pem ec2-user@<your-instance-IP>`
2. Navigate to the `src/` directory of this repository
    - `cd path/to/ds4300-final-project/src`
3. Clear the RDS instance (optional)
    - `python reset.py`
4. Run the main script using Streamlit
    - `streamlit run main.py`