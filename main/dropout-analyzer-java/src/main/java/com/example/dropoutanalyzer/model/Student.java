package com.example.dropoutanalyzer.model;

import javax.persistence.*;
import java.util.List;

@Entity
@Table(name = "student")
public class Student {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String username;

    @Column(name = "stud_name", nullable = false)
    private String studName;

    private String gender;

    private String dob;

    private String status;

    @Column(name = "sslc_marks")
    private String sslcMarks;

    @Column(name = "hsc_marks")
    private String hscMarks;

    @Column(name = "clg_name")
    private String clgName;

    @Column(name = "mother_name")
    private String motherName;

    @Column(name = "father_name")
    private String fatherName;

    @Column(columnDefinition = "TEXT")
    private String address;

    @OneToMany(mappedBy = "student", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<UniversityMarks> universityMarks;

    @OneToOne(mappedBy = "student", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private DropoutStudentDetails dropoutDetails;

    // Default constructor
    public Student() {}

    // Constructor with all fields
    public Student(Long id, String username, String studName, String gender, String dob, String status,
                   String sslcMarks, String hscMarks, String clgName, String motherName, String fatherName,
                   String address, List<UniversityMarks> universityMarks, DropoutStudentDetails dropoutDetails) {
        this.id = id;
        this.username = username;
        this.studName = studName;
        this.gender = gender;
        this.dob = dob;
        this.status = status;
        this.sslcMarks = sslcMarks;
        this.hscMarks = hscMarks;
        this.clgName = clgName;
        this.motherName = motherName;
        this.fatherName = fatherName;
        this.address = address;
        this.universityMarks = universityMarks;
        this.dropoutDetails = dropoutDetails;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getStudName() {
        return studName;
    }

    public void setStudName(String studName) {
        this.studName = studName;
    }

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public String getDob() {
        return dob;
    }

    public void setDob(String dob) {
        this.dob = dob;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getSslcMarks() {
        return sslcMarks;
    }

    public void setSslcMarks(String sslcMarks) {
        this.sslcMarks = sslcMarks;
    }

    public String getHscMarks() {
        return hscMarks;
    }

    public void setHscMarks(String hscMarks) {
        this.hscMarks = hscMarks;
    }

    public String getClgName() {
        return clgName;
    }

    public void setClgName(String clgName) {
        this.clgName = clgName;
    }

    public String getMotherName() {
        return motherName;
    }

    public void setMotherName(String motherName) {
        this.motherName = motherName;
    }

    public String getFatherName() {
        return fatherName;
    }

    public void setFatherName(String fatherName) {
        this.fatherName = fatherName;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public List<UniversityMarks> getUniversityMarks() {
        return universityMarks;
    }

    public void setUniversityMarks(List<UniversityMarks> universityMarks) {
        this.universityMarks = universityMarks;
    }

    public DropoutStudentDetails getDropoutDetails() {
        return dropoutDetails;
    }

    public void setDropoutDetails(DropoutStudentDetails dropoutDetails) {
        this.dropoutDetails = dropoutDetails;
    }
}
