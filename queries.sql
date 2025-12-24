create database hospital;
use hospital;
-- create
CREATE TABLE patient (
  id varchar(50) primary key,
  name varchar(50) not null,
  gender varchar(50) not null,
  age int not null,
  blood_group varchar(3) not null, 
  contact int not null
);

CREATE TABLE doctor(
  id VARCHAR(50) PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  gender VARCHAR(10),
  dob DATE,
  specialization VARCHAR(50),
  experience INT,
  contact INT,
  email VARCHAR(100),
  consultation_fee INT,
  dept_id VARCHAR(50)
);

CREATE TABLE appointments (
  id VARCHAR(50) PRIMARY KEY not null,
  patient_id VARCHAR(50) not null,
  doctor_id VARCHAR(50) not null,
  appointment_date DATE,
  appointment_time TIME,
  reason VARCHAR(255),
  status VARCHAR(20),

  FOREIGN KEY (patient_id) REFERENCES patient(id),
  FOREIGN KEY (doctor_id) REFERENCES doctor(id)
);
