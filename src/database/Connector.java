/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package database;

import java.sql.Connection;
import java.sql.DriverManager;

/**
 *
 * @author pj
 */
public class Connector {
    
    public Connector(){
        
    }
    public Connection myConn(){
        
           Connection conn;
        try {
            
            Class.forName("com.mysql.cj.jdbc.Driver");
            conn = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/monitoring_system", "root", "");
            System.out.println("Connected to Database!");
            return conn;
        } catch (Exception e) {
            System.out.println("Connection Error: " + e.getMessage());
            return null;
        }
        
    }
}
  
