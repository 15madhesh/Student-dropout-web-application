package com.example.dropoutanalyzer.model;

import javax.persistence.*;

@Entity
@Table(name = "university_marks")
public class UniversityMarks {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "student_id", nullable = false)
    private Student student;

    private Integer semester;

    // Internal 1 marks
    @Column(name = "internal1_sub1")
    private Double internal1Sub1;

    @Column(name = "internal1_sub2")
    private Double internal1Sub2;

    @Column(name = "internal1_sub3")
    private Double internal1Sub3;

    @Column(name = "internal1_sub4")
    private Double internal1Sub4;

    @Column(name = "internal1_sub5")
    private Double internal1Sub5;

    @Column(name = "internal1_sub6")
    private Double internal1Sub6;

    // Internal 2 marks
    @Column(name = "internal2_sub1")
    private Double internal2Sub1;

    @Column(name = "internal2_sub2")
    private Double internal2Sub2;

    @Column(name = "internal2_sub3")
    private Double internal2Sub3;

    @Column(name = "internal2_sub4")
    private Double internal2Sub4;

    @Column(name = "internal2_sub5")
    private Double internal2Sub5;

    @Column(name = "internal2_sub6")
    private Double internal2Sub6;

    // Internal 3 marks
    @Column(name = "internal3_sub1")
    private Double internal3Sub1;

    @Column(name = "internal3_sub2")
    private Double internal3Sub2;

    @Column(name = "internal3_sub3")
    private Double internal3Sub3;

    @Column(name = "internal3_sub4")
    private Double internal3Sub4;

    @Column(name = "internal3_sub5")
    private Double internal3Sub5;

    @Column(name = "internal3_sub6")
    private Double internal3Sub6;

    private Double cgpa;

    // Default constructor
    public UniversityMarks() {}

    // Constructor with all fields
    public UniversityMarks(Long id, Student student, Integer semester, Double internal1Sub1, Double internal1Sub2,
                          Double internal1Sub3, Double internal1Sub4, Double internal1Sub5, Double internal1Sub6,
                          Double internal2Sub1, Double internal2Sub2, Double internal2Sub3, Double internal2Sub4,
                          Double internal2Sub5, Double internal2Sub6, Double internal3Sub1, Double internal3Sub2,
                          Double internal3Sub3, Double internal3Sub4, Double internal3Sub5, Double internal3Sub6,
                          Double cgpa) {
        this.id = id;
        this.student = student;
        this.semester = semester;
        this.internal1Sub1 = internal1Sub1;
        this.internal1Sub2 = internal1Sub2;
        this.internal1Sub3 = internal1Sub3;
        this.internal1Sub4 = internal1Sub4;
        this.internal1Sub5 = internal1Sub5;
        this.internal1Sub6 = internal1Sub6;
        this.internal2Sub1 = internal2Sub1;
        this.internal2Sub2 = internal2Sub2;
        this.internal2Sub3 = internal2Sub3;
        this.internal2Sub4 = internal2Sub4;
        this.internal2Sub5 = internal2Sub5;
        this.internal2Sub6 = internal2Sub6;
        this.internal3Sub1 = internal3Sub1;
        this.internal3Sub2 = internal3Sub2;
        this.internal3Sub3 = internal3Sub3;
        this.internal3Sub4 = internal3Sub4;
        this.internal3Sub5 = internal3Sub5;
        this.internal3Sub6 = internal3Sub6;
        this.cgpa = cgpa;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Student getStudent() {
        return student;
    }

    public void setStudent(Student student) {
        this.student = student;
    }

    public Integer getSemester() {
        return semester;
    }

    public void setSemester(Integer semester) {
        this.semester = semester;
    }

    public Double getInternal1Sub1() {
        return internal1Sub1;
    }

    public void setInternal1Sub1(Double internal1Sub1) {
        this.internal1Sub1 = internal1Sub1;
    }

    public Double getInternal1Sub2() {
        return internal1Sub2;
    }

    public void setInternal1Sub2(Double internal1Sub2) {
        this.internal1Sub2 = internal1Sub2;
    }

    public Double getInternal1Sub3() {
        return internal1Sub3;
    }

    public void setInternal1Sub3(Double internal1Sub3) {
        this.internal1Sub3 = internal1Sub3;
    }

    public Double getInternal1Sub4() {
        return internal1Sub4;
    }

    public void setInternal1Sub4(Double internal1Sub4) {
        this.internal1Sub4 = internal1Sub4;
    }

    public Double getInternal1Sub5() {
        return internal1Sub5;
    }

    public void setInternal1Sub5(Double internal1Sub5) {
        this.internal1Sub5 = internal1Sub5;
    }

    public Double getInternal1Sub6() {
        return internal1Sub6;
    }

    public void setInternal1Sub6(Double internal1Sub6) {
        this.internal1Sub6 = internal1Sub6;
    }

    public Double getInternal2Sub1() {
        return internal2Sub1;
    }

    public void setInternal2Sub1(Double internal2Sub1) {
        this.internal2Sub1 = internal2Sub1;
    }

    public Double getInternal2Sub2() {
        return internal2Sub2;
    }

    public void setInternal2Sub2(Double internal2Sub2) {
        this.internal2Sub2 = internal2Sub2;
    }

    public Double getInternal2Sub3() {
        return internal2Sub3;
    }

    public void setInternal2Sub3(Double internal2Sub3) {
        this.internal2Sub3 = internal2Sub3;
    }

    public Double getInternal2Sub4() {
        return internal2Sub4;
    }

    public void setInternal2Sub4(Double internal2Sub4) {
        this.internal2Sub4 = internal2Sub4;
    }

    public Double getInternal2Sub5() {
        return internal2Sub5;
    }

    public void setInternal2Sub5(Double internal2Sub5) {
        this.internal2Sub5 = internal2Sub5;
    }

    public Double getInternal2Sub6() {
        return internal2Sub6;
    }

    public void setInternal2Sub6(Double internal2Sub6) {
        this.internal2Sub6 = internal2Sub6;
    }

    public Double getInternal3Sub1() {
        return internal3Sub1;
    }

    public void setInternal3Sub1(Double internal3Sub1) {
        this.internal3Sub1 = internal3Sub1;
    }

    public Double getInternal3Sub2() {
        return internal3Sub2;
    }

    public void setInternal3Sub2(Double internal3Sub2) {
        this.internal3Sub2 = internal3Sub2;
    }

    public Double getInternal3Sub3() {
        return internal3Sub3;
    }

    public void setInternal3Sub3(Double internal3Sub3) {
        this.internal3Sub3 = internal3Sub3;
    }

    public Double getInternal3Sub4() {
        return internal3Sub4;
    }

    public void setInternal3Sub4(Double internal3Sub4) {
        this.internal3Sub4 = internal3Sub4;
    }

    public Double getInternal3Sub5() {
        return internal3Sub5;
    }

    public void setInternal3Sub5(Double internal3Sub5) {
        this.internal3Sub5 = internal3Sub5;
    }

    public Double getInternal3Sub6() {
        return internal3Sub6;
    }

    public void setInternal3Sub6(Double internal3Sub6) {
        this.internal3Sub6 = internal3Sub6;
    }

    public Double getCgpa() {
        return cgpa;
    }

    public void setCgpa(Double cgpa) {
        this.cgpa = cgpa;
    }
}
