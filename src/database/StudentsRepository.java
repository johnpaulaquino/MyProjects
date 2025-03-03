/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package database;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.ResultSet;

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
            String station) throws SQLException {

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
            ps1.execute();
            this.conn.commit();
        } catch (SQLException e) {
            this.conn.rollback();
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
        } catch (Exception e) {
        }

        return studentIdFromDb;
    }

    public boolean addStudents(
            String studentId,
            String studentName,
            int yearLevel,
            String section,
            String strand,
            String contact_no,
            String address,
            String station) throws SQLException {
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
            ps1.execute();
            this.conn.commit();
            String studentIdFromDb = this.getUserId(studentId);

            this.add_additional_info(studentIdFromDb, contact_no, address, station);
            
            return true;
        } catch (SQLException e) {
            System.out.println("An error Occured: " + e.getMessage());
            this.conn.rollback();
            return false;
        } finally {
        }
    }
    public ResultSet getStudentsRecords(String strand, int yearLevel, String section){
        PreparedStatement ps1;
        ResultSet rs;
        String stmt1 = "SELECT s.id, s.student_id, s.student_name,"
                + "s.year_level, s.section, s.strand,a.contact_no, a.address, "
                + "a.station "
                + "FROM students as s "
                + "INNER JOIN add_info as a "
                + "ON s.id = a.students_id "
                + "WHERE s.year_level = ? "
                + "AND s.section = ? "
                + "AND s.strand = ?";
        try {
            ps1 = this.conn.prepareStatement(stmt1);
            
            ps1.setInt(1, yearLevel);
            ps1.setString(2, section);
            ps1.setString(3, strand);
            
            rs = ps1.executeQuery();
  
            return rs;
            
        } catch (SQLException e) {
        }
        return null;
    }
    
      public void closeConnection() {
        try {
            if (this.conn != null && !this.conn.isClosed()) {
                conn.close();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
      }
     public int countValues(String strand, String section, int yearLevel){
         PreparedStatement ps ;
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
             if (rs.next()){
                 count = rs.getInt("count(id)");
                 return count;
             }
         } catch (SQLException e) {
         } finally {
         }
         
         return 1;
     }
    public static void main(String[] args) {
        StudentsRepository std = new StudentsRepository();


    }
}
