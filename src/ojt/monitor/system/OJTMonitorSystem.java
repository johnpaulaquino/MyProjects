/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package ojt.monitor.system;

import database.StudentsRepository;
import java.text.SimpleDateFormat;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.Date;

/**
 *
 * @author vhalv
 */
public class OJTMonitorSystem {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        var sRepo = new StudentsRepository();
        try {
            sRepo.studentTimeIn("SHS2", new Date(), LocalTime.now());
        } catch (Exception e) {
        }

    }
    
}
