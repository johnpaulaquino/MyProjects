/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package database;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.sql.Connection;
import java.sql.Date;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.ResultSet;
import java.sql.Time;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.HashMap;

import java.util.UUID;

/**
 *
 * @author pj
 */
public class StudentsRepository {

    private Connection conn;

    public StudentsRepository() {
        conn = new Connector().myConn();

    }

    private void add_additional_info(
            String student_id,
            String contact_no,
            String address,
            String station) throws SQLException, FileNotFoundException {

        PreparedStatement ps1;

        String stmt1 = "INSERT INTO add_info"
                + "(students_id, contact_no, address,station) "
                + "VALUES(?,?,?,?)";

        try {

            ps1 = this.conn.prepareStatement(stmt1);

            ps1.setString(1, student_id);
            ps1.setString(2, contact_no);
            ps1.setString(3, address);
            ps1.setString(4, station);

            this.conn.setAutoCommit(false);

            ps1.executeUpdate();

            this.conn.commit();
        } catch (SQLException e) {
            this.conn.rollback();
        }

    }

    public void addStudentProfilePicture(String student_id, File file, String filename) throws FileNotFoundException, SQLException {
        PreparedStatement ps;

        String stmt = "INSERT INTO students_profile"
                + " (students_id, profile_picture, profile_name) "
                + "VALUES(?,?,?)";
        try {
            FileInputStream fis = new FileInputStream(file);

            ps = this.conn.prepareStatement(stmt);
            ps.setString(1, student_id);
            ps.setBlob(2, fis);
            ps.setString(3, filename);
            this.conn.setAutoCommit(false);
            ps.executeUpdate();
            this.conn.commit();

        } catch (SQLException e) {
            this.conn.rollback();
            System.out.println("An error Occurred: " + e.getMessage());
        } finally {
        }
    }

    public String getUserId(String studentId) {
        PreparedStatement ps1;
        ResultSet rs1;
        String studentIdFromDb = "";
        String queryStudentsInfo = "SELECT id "
                + "FROM students "
                + "WHERE student_id = ?";

        try {
            ps1 = this.conn.prepareStatement(queryStudentsInfo);
            ps1.setString(1, studentId);
            rs1 = ps1.executeQuery();

            if (rs1.next()) {

                studentIdFromDb = rs1.getString("id");

            }
        } catch (SQLException e) {
            System.out.println("An error Occurred " + e.getMessage());
        }

        return studentIdFromDb;
    }

    public void studentTimeIn(
            String studentId,
            java.util.Date todayDate,
            LocalTime timeIn) {

        String stmt = "INSERT INTO students_tracker (student_id, date_in, time_in) "
                + "Values (?,?,?)";

        try (var ps1 = conn.prepareStatement(stmt)) {
            
            ps1.setString(1, studentId);
            ps1.setDate(2, new Date(todayDate.getTime()));
            
            ps1.setTime(3, Time.valueOf(timeIn));
            int row = ps1.executeUpdate();
            
            if(row > 0){
                 System.out.println("Inserte");
            }else{
                System.out.println("Failed to insert");
            }
           
        } catch (Exception e) {
            System.out.println("An error occurred " + e.getMessage());
        }
    }

    public boolean studentTimeOut(String studentId, LocalTime timeout, String totalRendered) {
        String stmt = "UPdate students_tracker set time_out = ?, total_rendered = ?"
                + " Where student_id = ? and date_in = curdate() ";

        try (var ps1 = conn.prepareStatement(stmt)) {
            ps1.setTime(1, Time.valueOf(timeout));
            ps1.setString(2, totalRendered);
            ps1.setString(3, studentId);

            int row = ps1.executeUpdate();
            if (row > 0) {
                return true;
            }

        } catch (Exception e) {
            System.out.println("An error occured " + e.getMessage());
        }
        return false;
    }

    public HashMap<String, String> studentGetTimeIn(String userId) {
        /**
         * Retrieve the time in of the student via student_id and date today and
         * it will use this to calculate the total rendered time
         */
        String stmt = "Select time_in, time_out From students_tracker "
                + "Where student_id = ? and date_in = curdate()";
        HashMap<String, String> data = new HashMap<String, String>();
        try (var ps1 = conn.prepareStatement(stmt)) {
            ps1.setString(1, userId);
            try (var rs = ps1.executeQuery()) {
                if (rs.next()) {
                    data.put("time_in", rs.getTime("time_in").toString());
                    if (rs.getTime("time_out") != null) {
                        data.put("time_out", rs.getTime("time_out").toString());
                    }

                    return data;
                }
            } catch (Exception e) {
                System.out.println("An error occurred " + e.getMessage());
            }
        } catch (Exception e) {
            System.out.println("An error occurred " + e.getMessage());
        }

        return null;
    }

    public ResultSet getStudentTracker(String userId) {
        String stmt = "Select date_in, time_in, time_out "
                + "From students_tracker "
                + "where student_id = ?";
        try {
            var ps1 = conn.prepareStatement(stmt);
            ps1.setString(1, userId);
            var rs = ps1.executeQuery();
            return rs;
        } catch (Exception e) {
            System.out.println("An error occurred " + e.getMessage());
        }
        return null;
    }

    public boolean addStudents(
            String studentId,
            String studentName,
            int yearLevel,
            String section,
            String strand,
            String contact_no,
            String address,
            String station,
            File file,
            String filename) throws SQLException, FileNotFoundException {
        //Generate UUID for Students id
        UUID uuid = UUID.randomUUID();
        PreparedStatement ps1;
        PreparedStatement ps2;
        ResultSet rs1;

        String stmt1 = "INSERT INTO students"
                + "(id, student_id, student_name, year_level, section, strand)"
                + "VALUES (?,?,?,?,?,?)";

        try {
            ps1 = this.conn.prepareStatement(stmt1);
            ps1.setString(1, uuid.toString());
            ps1.setString(2, studentId);
            ps1.setString(3, studentName);
            ps1.setInt(4, yearLevel);
            ps1.setString(5, section);
            ps1.setString(6, strand);
            this.conn.setAutoCommit(false);
            ps1.executeUpdate();
            this.conn.commit();

            //Get the student unique identifier from db
            String studentIdFromDb = this.getUserId(studentId);

            this.add_additional_info(studentIdFromDb, contact_no, address, station);

            this.addStudentProfilePicture(studentIdFromDb, file, filename);

            return true;
        } catch (SQLException e) {
            System.out.println("An error Occured: " + e.getMessage());
            this.conn.rollback();
            return false;
        } finally {
        }
    }

    public ResultSet getStudentsRecords(String strand, int yearLevel, String section) {
        PreparedStatement ps1;
        ResultSet rs;
        String stmt1 = "SELECT s.id, s.student_id, s.student_name,"
                + "s.year_level, s.section, s.strand,a.contact_no, a.address, "
                + "a.station, CAST(SUM(tr.total_rendered) as char) as total_rendered "
                + "FROM students as s "
                + "INNER JOIN add_info as a "
                + "ON s.id = a.students_id "
                + "Left join students_tracker tr "
                + "ON s.student_id = tr.student_id "
                + "WHERE s.year_level = ? "
                + "AND s.section = ? "
                + "AND s.strand = ? "
                + "Group by s.student_id";
        try {
            ps1 = this.conn.prepareStatement(stmt1);

            ps1.setInt(1, yearLevel);
            ps1.setString(2, section);
            ps1.setString(3, strand);

            rs = ps1.executeQuery();

            return rs;

        } catch (SQLException e) {
            System.out.println("An error occurred " + e.getMessage());
        }
        return null;
    }

    public int countValues(String strand, String section, int yearLevel) {
        PreparedStatement ps;
        ResultSet rs;
        String stmt = "Select count(id) FROM students "
                + "WHERE year_level = ? and section = ? and strand = ?";
        int count = 0;
        try {
            ps = this.conn.prepareStatement(stmt);
            ps.setInt(1, yearLevel);
            ps.setString(2, section);
            ps.setString(3, strand);
            rs = ps.executeQuery();
            if (rs.next()) {
                count = rs.getInt("count(id)");
                return count;
            }
        } catch (SQLException e) {
            System.out.println("An error occurred " + e.getMessage());
        } finally {
        }

        return 1;
    }

    public void deleteStudents(String student_id) {
        String stmt1 = "DELETE FROM students "
                + "WHERE student_id = ?";

        PreparedStatement ps1;

        try {
            ps1 = this.conn.prepareStatement(stmt1);
            ps1.setString(1, student_id);
            int rowsAffected = ps1.executeUpdate();

            if (rowsAffected > 0) {

                System.out.println("Successfully Deleted!");

            } else {
                System.out.println("No records to delete");
            }

        } catch (SQLException e) {
            System.out.println("An error occurred " + e.getMessage());
        } finally {
        }
    }

    public ResultSet studentInformation(String student_id) {
        ResultSet rs;
        PreparedStatement ps;
        String stmt = "Select s.student_id, s.student_name, "
                + "s.year_level, s.section, s.strand, "
                + "a.contact_no, a.station, a.address,"
                + "p.profile_picture, p.profile_name, "
                + "tr.date_in, tr.time_in, tr.time_out "
                + "FROM students as s "
                + "INNER JOIN add_info as a "
                + "ON s.id = a.students_id "
                + "INNER JOIN students_profile as p "
                + "ON s.id = p.students_id "
                + "LEFT JOIN students_tracker tr "
                + "ON s.student_id = tr.student_id "
                + "WHERE s.student_id = ?";
        try {
            ps = this.conn.prepareStatement(stmt);
            ps.setString(1, student_id);

            rs = ps.executeQuery();

            return rs;

        } catch (SQLException e) {
            System.out.println("An error occurred " + e.getMessage());
        }
        return null;

    }

}
