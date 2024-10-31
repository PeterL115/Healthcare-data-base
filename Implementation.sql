-- use Healthcaredb;

-- CREATE INDEX Department_name ON Department(DepartmentName);
-- show INDEX FROM Department;

-- CREATE INDEX Staff_role ON Staff(Role);
-- show INDEX FROM Staff;

-- CREATE VIEW Patient_Appointment AS
-- SELECT 
--     CONCAT(p.FirstName, ' ', p.LastName) AS PFullName, 
--     CONCAT(d.FirstName, ' ', d.LastName) AS DFullName, 
--     a.AppointmentDate, a.AppointmentTime, a.Status
-- FROM Patient p, Doctor d, Appointment a
-- WHERE 
--     p.PatientID = a.PatientID AND d.DoctorID = a.DoctorID;

-- SELECT * FROM Patient_Appointment;

-- CREATE TEMPORARY TABLE TempPatient (
--     PatientID INT PRIMARY KEY,
--     FirstName VARCHAR(50),
--     LastName VARCHAR(50),
--     DateOfBirth DATE,
--     Gender VARCHAR(10),
--     Address VARCHAR(100),
--     PhoneNumber VARCHAR(20),
--     Email VARCHAR(100)
-- );

-- INSERT INTO TempPatient(PatientID, FirstName, LastName, DateOfBirth, Gender, Address, PhoneNumber, Email)
-- SELECT PatientID, FirstName, LastName, DateOfBirth, Gender, Address, PhoneNumber, Email
-- FROM Patient
-- LIMIT 6;

-- SELECT * FROM TempPatient;

-- DELIMITER //
-- CREATE TRIGGER check_appointment_conflict
-- BEFORE INSERT ON Appointment
-- FOR EACH ROW
-- BEGIN
--     IF EXISTS (
--         SELECT 1 
--         FROM Appointment 
--         WHERE DoctorID = NEW.DoctorID 
--         AND AppointmentDate = NEW.AppointmentDate 
--         AND AppointmentTime = NEW.AppointmentTime
--     ) THEN
--         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Appointment conflict: The doctor is already booked for this time slot.';
--     END IF;
-- END//
-- DELIMITER ;

-- INSERT INTO Appointment (PatientID, DoctorID, AppointmentDate, AppointmentTime, Reason, Status) VALUES
-- (6, 1, '2024-09-06', '10:30', 'Follow-up consultation', 'Scheduled');


-- DELIMITER //

-- CREATE PROCEDURE CountAppointments(
--     IN p_DoctorID INT,
--     OUT p_AppointmentCount INT
-- )
-- BEGIN
--     SELECT COUNT(*) INTO p_AppointmentCount
--     FROM Appointment
--     WHERE DoctorID = p_DoctorID;
-- END//
-- DELIMITER ;

-- CALL CountAppointments(6, @count);
-- SELECT @count;

-- DELIMITER //
-- CREATE PROCEDURE GetPatientDetails(IN pPatientID INT)
-- BEGIN
--     SELECT * FROM Patient WHERE PatientID = pPatientID;
-- END//
-- DELIMITER ;

-- CALL GetPatientDetails(7);

DELIMITER //
CREATE FUNCTION CalculateAge(patientID INT) RETURNS INT
BEGIN
    DECLARE dob DATE;
    -- Get the date of birth for the patient, ensuring only one row is selected
    SELECT DateOfBirth INTO dob 
    FROM Patient 
    WHERE PatientID = patientID 
    LIMIT 1;
    -- Calculate and return the age
    RETURN TIMESTAMPDIFF(YEAR, dob, CURDATE());
END//
DELIMITER ;

SELECT CalculateAge(1);