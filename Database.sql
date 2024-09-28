DROP DATABASE IF EXISTS `ssis_web_database`;

#create the database
CREATE DATABASE `ssis_web_database`;	

#Use the databse
USE `ssis_web_database`;					

#Create the tables
CREATE TABLE `colleges`(	-- table for colleges
	`code` VARCHAR(5) NOT NULL,
	`name` VARCHAR(100) NOT NULL,
	CONSTRAINT `pk_college_code` PRIMARY KEY(`code`),
   CONSTRAINT `unique_college_name` UNIQUE(`name`)
);

CREATE TABLE `programs`(	-- table for programs
	`code` VARCHAR(10) NOT NULL,
   `name` VARCHAR(100) NOT NULL,
   `college_code` VARCHAR(5) NOT NULL,	-- it is not possible to have a program without a college
   CONSTRAINT `pk_program_code` PRIMARY KEY(`code`),
   CONSTRAINT `unique_program_name` UNIQUE(`name`),
   CONSTRAINT `fk_program_college` FOREIGN KEY (`college_code`) REFERENCES `colleges`(`code`) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE `students`(	-- table for students
	`student_id` CHAR(9) NOT NULL,
	`first_name` VARCHAR(50) NOT NULL,
	`last_name` VARCHAR(50) NOT NULL,
	`program_code`VARCHAR(10),
	`year_level` ENUM("1st year", "2nd year", "3rd year", "4th year", "More...") NOT NULL,
	`gender` VARCHAR(50) NOT NULL,
	CONSTRAINT `pk_student_id` PRIMARY KEY(`student_id`),
	CONSTRAINT `unique_name` UNIQUE(`first_name`, `last_name`),
	CONSTRAINT `fk_student_program` FOREIGN KEY(`program_code`) REFERENCES `programs`(`code`) ON UPDATE CASCADE ON DELETE SET NULL
);

# Populate the `colleges` table 
INSERT INTO `colleges` VALUES ("CCS", "College of Computer Studies"),
										("COE", "College of Enginnering"),
										("CEBA", "College of Economics, Business and Accountancy"),
										("CSM", "College of Science and Mathematics"),
										("CED", "College of Education"),
										("CASS", "College of Arts and Social Sciences"),
										("CHS", "College of Health Sciences");

# Populate the `programs` table																				
INSERT INTO `programs` VALUE 	("BSCS", "Bachelor of Science in Computer Science", "CCS"),
										("BSCA", "Bachelor of Science in Computer Applications", "CCS"),
										("BSIT", "Bachelor of Science in Information Technology", "CCS"),
										("BSIS", "Bachelor of Science in Information Systems", "CCS"),
										("BSEM", "Bachelor of Science in Mining Engineering", "COE"),										
										("BSA", "Bachelor of Science in Accountancy", "CEBA"),
										("BSStat", "Bachelor of Science in Statistics", "CSM"),
										("BEEd", "Bachelor of Elementary Education", "CED"),
										("BSPsy", "Bachelor of Science in Psychology", "CASS"),
										("BSN", "Bachelor of Science in Nursing", "CHS");

# Populate the `students` table
INSERT INTO `students` VALUE ("2022-0378", "Caine Ivan", "Bautista", "BSCS", "3rd Year", "Male");
INSERT INTO `students` VALUE ("2018-2041", "Joshua", "Gapol", "BSIT", "4th Year", "Gay");
INSERT INTO `students` VALUE ("2022-0542", "John 3:16", "Ventura", "BSA", "3rd Year", "Ladyboy");
INSERT INTO `students` VALUE ("2022-3337", "Angel", "Cabilla", "BSPsy", "3rd Year", "Likes Breb");
INSERT INTO `students` (`student_id`, `first_name`, `last_name`, `program_code`, `year_level`, `gender`) VALUES
-- 10 students for BSCS
('2024-0001', 'John', 'Doe', 'BSCS', '1st Year', 'Male'),
('2024-0002', 'Jane', 'Smith', 'BSCS', '2nd Year', 'Female'),
('2024-0003', 'Michael', 'Johnson', 'BSCS', '3rd Year', 'Male'),
('2024-0004', 'Emily', 'Williams', 'BSCS', '4th Year', 'Female'),
('2024-0005', 'Matthew', 'Brown', 'BSCS', '1st Year', 'Male'),
('2024-0006', 'Olivia', 'Jones', 'BSCS', '2nd Year', 'Female'),
('2024-0007', 'Daniel', 'Garcia', 'BSCS', '3rd Year', 'Male'),
('2024-0008', 'Sophia', 'Martinez', 'BSCS', '4th Year', 'Female'),
('2024-0009', 'David', 'Hernandez', 'BSCS', '1st Year', 'Male'),
('2024-0010', 'Emma', 'Lopez', 'BSCS', '2nd Year', 'Female'),

-- 10 students for BSCA
('2024-0011', 'James', 'Wilson', 'BSCA', '1st Year', 'Male'),
('2024-0012', 'Ava', 'Anderson', 'BSCA', '2nd Year', 'Female'),
('2024-0013', 'Ethan', 'Thomas', 'BSCA', '3rd Year', 'Male'),
('2024-0014', 'Isabella', 'Taylor', 'BSCA', '4th Year', 'Female'),
('2024-0015', 'Alexander', 'Moore', 'BSCA', '1st Year', 'Male'),
('2024-0016', 'Mia', 'Jackson', 'BSCA', '2nd Year', 'Female'),
('2024-0017', 'William', 'Martin', 'BSCA', '3rd Year', 'Male'),
('2024-0018', 'Charlotte', 'Lee', 'BSCA', '4th Year', 'Female'),
('2024-0019', 'Benjamin', 'Perez', 'BSCA', '1st Year', 'Male'),
('2024-0020', 'Amelia', 'White', 'BSCA', '2nd Year', 'Female'),

-- 10 students for BSIT
('2024-0021', 'Lucas', 'Thompson', 'BSIT', '1st Year', 'Male'),
('2024-0022', 'Evelyn', 'Harris', 'BSIT', '2nd Year', 'Female'),
('2024-0023', 'Mason', 'Clark', 'BSIT', '3rd Year', 'Male'),
('2024-0024', 'Harper', 'Lewis', 'BSIT', '4th Year', 'Female'),
('2024-0025', 'Noah', 'Robinson', 'BSIT', '1st Year', 'Male'),
('2024-0026', 'Ella', 'Walker', 'BSIT', '2nd Year', 'Female'),
('2024-0027', 'Jacob', 'Hall', 'BSIT', '3rd Year', 'Male'),
('2024-0028', 'Grace', 'Allen', 'BSIT', '4th Year', 'Female'),
('2024-0029', 'Logan', 'Young', 'BSIT', '1st Year', 'Male'),
('2024-0030', 'Zoe', 'King', 'BSIT', '2nd Year', 'Female'),

-- 10 students for BSIS
('2024-0031', 'Henry', 'Wright', 'BSIS', '1st Year', 'Male'),
('2024-0032', 'Nora', 'Scott', 'BSIS', '2nd Year', 'Female'),
('2024-0033', 'Sebastian', 'Torres', 'BSIS', '3rd Year', 'Male'),
('2024-0034', 'Lily', 'Nguyen', 'BSIS', '4th Year', 'Female'),
('2024-0035', 'Jack', 'Adams', 'BSIS', '1st Year', 'Male'),
('2024-0036', 'Aria', 'Baker', 'BSIS', '2nd Year', 'Female'),
('2024-0037', 'Owen', 'Gonzalez', 'BSIS', '3rd Year', 'Male'),
('2024-0038', 'Ella', 'Nelson', 'BSIS', '4th Year', 'Female'),
('2024-0039', 'Daniel', 'Carter', 'BSIS', '1st Year', 'Male'),
('2024-0040', 'Scarlett', 'Mitchell', 'BSIS', '2nd Year', 'Female'),

-- 10 students for BSEM
('2024-0041', 'Matthew', 'Perez', 'BSEM', '1st Year', 'Male'),
('2024-0042', 'Hannah', 'Roberts', 'BSEM', '2nd Year', 'Female'),
('2024-0043', 'Christopher', 'Turner', 'BSEM', '3rd Year', 'Male'),
('2024-0044', 'Megan', 'Phillips', 'BSEM', '4th Year', 'Female'),
('2024-0045', 'James', 'Cruz', 'BSEM', '1st Year', 'Male'),
('2024-0046', 'Natalie', 'Gray', 'BSEM', '2nd Year', 'Female'),
('2024-0047', 'John', 'Ramirez', 'BSEM', '3rd Year', 'Male'),
('2024-0048', 'Samantha', 'James', 'BSEM', '4th Year', 'Female'),
('2024-0049', 'Ethan', 'Watson', 'BSEM', '1st Year', 'Male'),
('2024-0050', 'Lily', 'Brooks', 'BSEM', '2nd Year', 'Female'),

-- 10 students for BSA
('2024-0051', 'Aiden', 'Hayes', 'BSA', '1st Year', 'Male'),
('2024-0052', 'Zara', 'Hughes', 'BSA', '2nd Year', 'Female'),
('2024-0053', 'Ryan', 'Butler', 'BSA', '3rd Year', 'Male'),
('2024-0054', 'Layla', 'Ward', 'BSA', '4th Year', 'Female'),
('2024-0055', 'Andrew', 'Graham', 'BSA', '1st Year', 'Male'),
('2024-0056', 'Aurora', 'Flores', 'BSA', '2nd Year', 'Female'),
('2024-0057', 'Eli', 'Jenkins', 'BSA', '3rd Year', 'Male'),
('2024-0058', 'Hannah', 'Morgan', 'BSA', '4th Year', 'Female'),
('2024-0059', 'Noah', 'Bell', 'BSA', '1st Year', 'Male'),
('2024-0060', 'Bella', 'Murphy', 'BSA', '2nd Year', 'Female'),

-- 10 students for BSStat
('2024-0061', 'Liam', 'Rivera', 'BSStat', '1st Year', 'Male'),
('2024-0062', 'Sophia', 'Cooper', 'BSStat', '2nd Year', 'Female'),
('2024-0063', 'James', 'Richardson', 'BSStat', '3rd Year', 'Male'),
('2024-0064', 'Mia', 'Cox', 'BSStat', '4th Year', 'Female'),
('2024-0065', 'Jackson', 'Watson', 'BSStat', '1st Year', 'Male'),
('2024-0066', 'Charlotte', 'Brooks', 'BSStat', '2nd Year', 'Female'),
('2024-0067', 'Matthew', 'Cox', 'BSStat', '3rd Year', 'Male'),
('2024-0068', 'Emily', 'Gray', 'BSStat', '4th Year', 'Female'),
('2024-0069', 'Aiden', 'Howard', 'BSStat', '1st Year', 'Male'),
('2024-0070', 'Zoe', 'Sanchez', 'BSStat', '2nd Year', 'Female'),

-- 10 students for BEEd
('2024-0071', 'Sebastian', 'Diaz', 'BEEd', '1st Year', 'Male'),
('2024-0072', 'Chloe', 'Hughes', 'BEEd', '2nd Year', 'Female'),
('2024-0073', 'Henry', 'Cox', 'BEEd', '3rd Year', 'Male'),
('2024-0074', 'Sofia', 'Flores', 'BEEd', '4th Year', 'Female'),
('2024-0075', 'Daniel', 'Ward', 'BEEd', '1st Year', 'Male'),
('2024-0076', 'Ella', 'Davis', 'BEEd', '2nd Year', 'Female'),
('2024-0077', 'Matthew', 'Young', 'BEEd', '3rd Year', 'Male'),
('2024-0078', 'Ava', 'Adams', 'BEEd', '4th Year', 'Female'),
('2024-0079', 'Samuel', 'Nelson', 'BEEd', '1st Year', 'Male'),
('2024-0080', 'Isabella', 'Parker', 'BEEd', '2nd Year', 'Female'),

-- 10 students for BSPsy
('2024-0081', 'Logan', 'Bennett', 'BSPsy', '1st Year', 'Male'),
('2024-0082', 'Mia', 'Collins', 'BSPsy', '2nd Year', 'Female'),
('2024-0083', 'Alexander', 'Murphy', 'BSPsy', '3rd Year', 'Male'),
('2024-0084', 'Emma', 'Russell', 'BSPsy', '4th Year', 'Female'),
('2024-0085', 'James', 'Ward', 'BSPsy', '1st Year', 'Male'),
('2024-0086', 'Charlotte', 'Watson', 'BSPsy', '2nd Year', 'Female'),
('2024-0087', 'William', 'James', 'BSPsy', '3rd Year', 'Male'),
('2024-0088', 'Ava', 'Cook', 'BSPsy', '4th Year', 'Female'),
('2024-0089', 'Benjamin', 'Harris', 'BSPsy', '1st Year', 'Male'),
('2024-0090', 'Sophia', 'Lee', 'BSPsy', '2nd Year', 'Female'),

-- 10 students for BSN
('2024-0091', 'Jacob', 'Young', 'BSN', '1st Year', 'Male'),
('2024-0092', 'Avery', 'Baker', 'BSN', '2nd Year', 'Female'),
('2024-0093', 'Mason', 'Harris', 'BSN', '3rd Year', 'Male'),
('2024-0094', 'Ella', 'Bell', 'BSN', '4th Year', 'Female'),
('2024-0095', 'Ethan', 'Lee', 'BSN', '1st Year', 'Male'),
('2024-0096', 'Olivia', 'Scott', 'BSN', '2nd Year', 'Female'),
('2024-0097', 'Daniel', 'Adams', 'BSN', '3rd Year', 'Male'),
('2024-0098', 'Mia', 'Thomas', 'BSN', '4th Year', 'Female'),
('2024-0099', 'Henry', 'Mitchell', 'BSN', '1st Year', 'Male'),
('2024-0100', 'Arianna', 'Walker', 'BSN', '2nd Year', 'Female');

