-- Database initialization script for AI Resume Screening system
-- Run this script after creating the database specified in .env

-- Create HR table to store current job position requirement and description
CREATE TABLE IF NOT EXISTS HR (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Position VARCHAR(255) NOT NULL,
    Experience INT,
    job_description LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create skills table to map positions to required skills (keeping for backward compatibility)
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    position VARCHAR(255) NOT NULL UNIQUE,
    skill TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create employees table to store shortlisted resumes with enhanced matching
CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255),
    Resume LONGTEXT,
    score FLOAT,
    location VARCHAR(255),
    category VARCHAR(255),
    match_percentage FLOAT,
    missing_skills TEXT,
    position_applied_for VARCHAR(255),
    mobile_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_score (score),
    INDEX idx_match_percentage (match_percentage),
    INDEX idx_email (Email),
    INDEX idx_position (position_applied_for)
);

-- Create applications history table for tracking all candidate applications
CREATE TABLE IF NOT EXISTS applications_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_email VARCHAR(255) NOT NULL,
    candidate_name VARCHAR(255) NOT NULL,
    position_applied_for VARCHAR(255) NOT NULL,
    match_percentage FLOAT,
    application_status ENUM('Applied', 'Under Review', 'Shortlisted', 'Interview', 'Rejected') DEFAULT 'Applied',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_candidate_email (candidate_email),
    INDEX idx_position (position_applied_for),
    INDEX idx_applied_at (applied_at)
);

-- Sample data for skills table (update as needed)
INSERT IGNORE INTO
    skills (position, skill)
VALUES (
        'python developer',
        'python, django, flask, fastapi, requests, pandas, numpy, scikit-learn'
    ),
    (
        'java developer',
        'java, spring, spring boot, maven, gradle, junit, hibernate'
    ),
    (
        'data science',
        'python, r, sql, machine learning, deep learning, tensorflow, pytorch, statistics'
    ),
    (
        'devops engineer',
        'docker, kubernetes, jenkins, aws, gcp, azure, terraform, ci/cd'
    ),
    (
        'web designing',
        'html, css, javascript, react, vue, figma, ui/ux, responsive design'
    );