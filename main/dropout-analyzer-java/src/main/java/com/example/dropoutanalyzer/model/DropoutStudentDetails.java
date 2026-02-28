package com.example.dropoutanalyzer.model;

import javax.persistence.*;

@Entity
@Table(name = "dropout_students")
public class DropoutStudentDetails {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "student_id", unique = true)
    private Student student;

    @Column(name = "disciplinary_action")
    private Boolean disciplinaryAction = false;

    @Column(name = "family_income")
    private String familyIncome;

    @Column(name = "fees_payment_status")
    private String feesPaymentStatus; // delayed, ontime, pending

    @Column(name = "educational_load")
    private Boolean educationalLoad = false;

    @Column(name = "part_time_work")
    private Boolean partTimeWork = false;

    @Column(name = "health_issue")
    private Boolean healthIssue = false;

    @Column(name = "health_issue_description", columnDefinition = "TEXT")
    private String healthIssueDescription;

    @Column(name = "day_scholar_or_hosteller")
    private String dayScholarOrHosteller; // day scholar or hosteller

    // Default constructor
    public DropoutStudentDetails() {}

    // Constructor with all fields
    public DropoutStudentDetails(Long id, Student student, Boolean disciplinaryAction, String familyIncome,
                                String feesPaymentStatus, Boolean educationalLoad, Boolean partTimeWork,
                                Boolean healthIssue, String healthIssueDescription, String dayScholarOrHosteller) {
        this.id = id;
        this.student = student;
        this.disciplinaryAction = disciplinaryAction;
        this.familyIncome = familyIncome;
        this.feesPaymentStatus = feesPaymentStatus;
        this.educationalLoad = educationalLoad;
        this.partTimeWork = partTimeWork;
        this.healthIssue = healthIssue;
        this.healthIssueDescription = healthIssueDescription;
        this.dayScholarOrHosteller = dayScholarOrHosteller;
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

    public Boolean getDisciplinaryAction() {
        return disciplinaryAction;
    }

    public void setDisciplinaryAction(Boolean disciplinaryAction) {
        this.disciplinaryAction = disciplinaryAction;
    }

    public String getFamilyIncome() {
        return familyIncome;
    }

    public void setFamilyIncome(String familyIncome) {
        this.familyIncome = familyIncome;
    }

    public String getFeesPaymentStatus() {
        return feesPaymentStatus;
    }

    public void setFeesPaymentStatus(String feesPaymentStatus) {
        this.feesPaymentStatus = feesPaymentStatus;
    }

    public Boolean getEducationalLoad() {
        return educationalLoad;
    }

    public void setEducationalLoad(Boolean educationalLoad) {
        this.educationalLoad = educationalLoad;
    }

    public Boolean getPartTimeWork() {
        return partTimeWork;
    }

    public void setPartTimeWork(Boolean partTimeWork) {
        this.partTimeWork = partTimeWork;
    }

    public Boolean getHealthIssue() {
        return healthIssue;
    }

    public void setHealthIssue(Boolean healthIssue) {
        this.healthIssue = healthIssue;
    }

    public String getHealthIssueDescription() {
        return healthIssueDescription;
    }

    public void setHealthIssueDescription(String healthIssueDescription) {
        this.healthIssueDescription = healthIssueDescription;
    }

    public String getDayScholarOrHosteller() {
        return dayScholarOrHosteller;
    }

    public void setDayScholarOrHosteller(String dayScholarOrHosteller) {
        this.dayScholarOrHosteller = dayScholarOrHosteller;
    }
}
