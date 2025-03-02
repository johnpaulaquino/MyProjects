/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package utils;

import com.mysql.cj.protocol.Resultset;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.UUID;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
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
        int i = 0;
        while (i <= resultSet) {            
            dft.addRow(new Object[]{
            studentId, studentName, addressStation, totalTimeRendered
            });
            i++;
        }
    }
    
    public static void main(String[] args) {
       
    }
     
}
