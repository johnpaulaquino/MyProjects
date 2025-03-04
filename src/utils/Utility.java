/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package utils;

import com.mysql.cj.protocol.Resultset;
import database.StudentsRepository;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.sql.ResultSet;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTabbedPane;
import javax.swing.JTable;
import javax.swing.table.DefaultTableModel;
import net.sourceforge.barbecue.Barcode;
import net.sourceforge.barbecue.BarcodeException;
import net.sourceforge.barbecue.BarcodeFactory;
import net.sourceforge.barbecue.BarcodeImageHandler;
import net.sourceforge.barbecue.output.OutputException;

/**
 *
 * @author pj
 */
public class Utility {
    
    
    public Utility(){
        
    }
    
    public boolean login(){
        
        return true;
    }
    
    public String validateTextField(
            String tfStudentName,
            String tfStudentId,
            String tfAddress,
            String tfStation,
            String cbSection,
            String tfContactNo){
        
        String message = "";
        if(tfStudentName.equals("")){
               message = "Student Name field must be filled!";
               return message;
           }
           else if(tfStudentId.equals("")){
              message =  "Student ID field must be filled!";
              return message;
           }
           else if(tfContactNo.equals("")){
              message = "Contact No. field must be filled!";
              return message;
           }
           else if(tfAddress.equals("")){
               message = "Address field must be filled!";
               return message;
           }
           
           else if(tfStation.equals("")){
               message ="Station field must be filled!";
               return message;
           }
           else if(cbSection.equals("Choose")){
               message =  "Grade and Section field must be filled!";
               return message;
           }
           if(!tfStudentId.matches("\\d+")){
               message = "Student Id Must be a number only!";
              return message; 
           }
           
           if(!tfContactNo.matches("\\d+")){
               message = "Contact No. Must be a number only!";
               return message;
           }
        return message;
        
    }
    private static void showBarcode(BufferedImage image) {
        JFrame frame = new JFrame("Barcode Example");
        frame.setSize(350, 200);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JLabel label = new JLabel(new ImageIcon(image));
        frame.add(label);
        
        frame.setVisible(true);
    }
    public void barCodeGenerator(String data) throws BarcodeException, OutputException, IOException{
        Barcode bd = BarcodeFactory.createCode128A(data);
        bd.setBarWidth(2); // Adjust width
        bd.setDrawingText(false);
        BarcodeImageHandler.savePNG(bd, new File("/home/pj/Downloads/barcode.png"));
    }
    
    public void setValueInTable(
            JTable tableName,
            String studentId,
            String studentName,
            String address,
            String station,
            String totalTimeRendered,
            int resultSet){
        DefaultTableModel dft = (DefaultTableModel) tableName.getModel();
        
        String addressStation = address + " " + station;
            dft.addRow(new Object[]{
            studentId, studentName, addressStation, totalTimeRendered});

       
    }
    
    public void refreshTable(
            JTabbedPane studentInfoTab,
            StudentsRepository repo,
            JTable tbIctHope,
            JTable tbIctLove,
            JTable tbHumssHope,
            JTable tbHumssLove,
            JTable tbHumssFaith,
            JTable tbAbmLove,
            JTable tbStemHope
    ){
        
      int selectedIndex = studentInfoTab.getSelectedIndex();
        String title = studentInfoTab.getTitleAt(selectedIndex);
        
        String slicedTitleTab [] = title.split(" ");
        
        String strand = slicedTitleTab[0];
        int yearLevel = Integer.parseInt(slicedTitleTab[1]);
        String section = slicedTitleTab[2];
        
        int count = repo.countValues(strand, section, yearLevel);
        
        
            Map<Integer, JTable> tableMap = new HashMap<>();
            tableMap.put(0, tbIctHope);
            tableMap.put(1, tbIctLove);
            tableMap.put(2, tbHumssHope);
            tableMap.put(3, tbHumssLove);
            tableMap.put(4, tbHumssFaith);
            tableMap.put(5, tbAbmLove);
            tableMap.put(6, tbStemHope);
        try {
            ResultSet rs = repo.getStudentsRecords(strand, yearLevel, section);
            DefaultTableModel dft = (DefaultTableModel) tableMap.get(selectedIndex).getModel();
            dft.setRowCount(0);
            while (rs.next()) {                
                 this.setValueInTable(
                         tableMap.get(selectedIndex), 
                         rs.getString("student_id"), 
                         rs.getString("student_name"), 
                         rs.getString("address"),
                         rs.getString("station"), 
                         section, 
                         count);
            }


        } catch (Exception e) {
        } finally {
        }
    }
    
    public static void main(String[] args) {
       
    }
     
}
