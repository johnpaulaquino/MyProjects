/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package utils;


import database.StudentsRepository;
import java.awt.Image;
import java.sql.Blob;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Map;
import javax.imageio.ImageIO;

import javax.swing.ImageIcon;
import javax.swing.JLabel;
import javax.swing.JTabbedPane;
import javax.swing.JTable;
import javax.swing.table.DefaultTableModel;

/**
 *
 * @author pj
 */
public class Utility {

    public Utility() {

    }

    public boolean login() {

        return true;
    }

    public String validateTextField(
            String tfStudentName,
            String tfStudentId,
            String tfAddress,
            String tfStation,
            String cbSection,
            String tfContactNo,
            String profilePath) {

        String message = "";
        if (tfStudentName.equals("")) {
            message = "Student Name field must be filled!";
            return message;
        } else if (tfStudentId.equals("")) {
            message = "Student ID field must be filled!";
            return message;
        } else if (tfContactNo.equals("")) {
            message = "Contact No. field must be filled!";
            return message;
        } else if (tfAddress.equals("")) {
            message = "Address field must be filled!";
            return message;
        } else if (tfStation.equals("")) {
            message = "Station field must be filled!";
            return message;
        } else if (cbSection.equals("Choose")) {
            message = "Grade and Section field must be filled!";
            return message;
        } else if (profilePath.equals("File Path")) {
            message = "Select profile image!";
            return message;
        }
        if (!tfStudentId.matches("\\d+")) {
            message = "Student Id Must be a number only!";
            return message;
        }

        if (!tfContactNo.matches("\\d+")) {
            message = "Contact No. Must be a number only!";
            return message;
        }

        String filePathSliced[] = profilePath.split("[.]");
        String fileExtension = filePathSliced[1];
        String fileExtensionsAllowed [] = {"png","jpeg","jpg",};
        
        boolean isExist = false;
        for (String extAllowed : fileExtensionsAllowed) {
            if(extAllowed.equals(fileExtension)){
                isExist= true;
            }
        }
        if(!isExist){
            message = "Invalid File extension!";
            
            return message;
        }
        
        
        return message;

    }
    public void setValueInTable(
            JTable tableName,
            String studentId,
            String studentName,
            String address,
            String station,
            String totalTimeRendered,
            int resultSet) {
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
    ) {

        int selectedIndex = studentInfoTab.getSelectedIndex();
        String title = studentInfoTab.getTitleAt(selectedIndex);

        String slicedTitleTab[] = title.split(" ");

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
    
    public void createTempFiles(String filename){
        try {
            Path folder = Paths.get(System.getProperty("user.dir"), "temp");
            
            if(!Files.exists(folder)){
                Files.createDirectories(folder);
            }
            Path filePath = folder.resolve(filename);
            Files.createFile(filePath);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        } finally {
        }
    }
    
    public byte[] getImageBytes(Blob blob, String rsString) throws SQLException, IOException{
        InputStream is = blob.getBinaryStream();
        byte bytes []= is.readAllBytes();
        
        return bytes;
    }
    
    public void setImageInLabel(JLabel label, byte imageBytes []) throws IOException{
        //Convert the bytes into BufferedImage
        ByteArrayInputStream byteArray = new ByteArrayInputStream(imageBytes);
        BufferedImage origImage = ImageIO.read(byteArray);
        
        Image scaledImage = origImage.getScaledInstance
                                (origImage.getWidth(), origImage.getHeight(), Image.SCALE_SMOOTH);
        
        ImageIcon icon = new ImageIcon(scaledImage);
        
        label.setIcon(icon);
       
    }

    public static void main(String[] args) {
        Utility utils = new Utility();

    }

}
