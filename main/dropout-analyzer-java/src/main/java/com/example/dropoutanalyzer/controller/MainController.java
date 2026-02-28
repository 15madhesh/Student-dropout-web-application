package com.example.dropoutanalyzer.controller;

import com.example.dropoutanalyzer.model.Student;
import com.example.dropoutanalyzer.model.UniversityMarks;
import com.example.dropoutanalyzer.model.DropoutStudentDetails;
import com.example.dropoutanalyzer.repository.StudentRepository;
import com.example.dropoutanalyzer.repository.UniversityMarksRepository;
import com.example.dropoutanalyzer.repository.DropoutStudentDetailsRepository;
import com.example.dropoutanalyzer.service.DropoutAnalysisService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Collectors;

@Controller
public class MainController {

    @Autowired
    private StudentRepository studentRepository;

    @Autowired
    private UniversityMarksRepository universityMarksRepository;

    @Autowired
    private DropoutStudentDetailsRepository dropoutStudentDetailsRepository;

    @Autowired
    private DropoutAnalysisService dropoutAnalysisService;

    private static final String UPLOAD_DIR = "uploads";

    @GetMapping("/")
    public String home() {
        return "redirect:/login";
    }

    @GetMapping("/login")
    public String login() {
        return "login";
    }

    // Remove this manual login method as Spring Security handles login now
    /*
    @PostMapping("/login")
    public String login(@RequestParam String username,
                       @RequestParam String password,
                       HttpSession session,
                       RedirectAttributes redirectAttributes) {
        username = username.trim();
        password = password.trim();

        // Check admin credentials
        if ("admin".equals(username) && "admin".equals(password)) {
            session.setAttribute("user", username);
            return "redirect:/dashboard";
        }

        // Check users.txt for other users (simplified for demo)
        try {
            Path usersFile = Paths.get("users.txt");
            if (Files.exists(usersFile)) {
                List<String> lines = Files.readAllLines(usersFile);
                for (String line : lines) {
                    String[] parts = line.trim().split(",", 2);
                    if (parts.length == 2) {
                        String fileUsername = parts[0].trim();
                        String filePassword = parts[1].trim();
                        if (fileUsername.equals(username) && filePassword.equals(password)) {
                            session.setAttribute("user", username);
                            return "redirect:/dashboard";
                        }
                    }
                }
            }
        } catch (IOException e) {
            // Handle file read error
        }

        redirectAttributes.addFlashAttribute("error", "Invalid Credentials");
        return "redirect:/login";
    }
    */

    @GetMapping("/dashboard")
    public String dashboard(HttpSession session, Model model) {
        String username = (String) session.getAttribute("user");
        if (username == null) {
            return "redirect:/login";
        }

        List<Student> students = studentRepository.findByUsername(username);
        model.addAttribute("students", students);
        return "dashboard";
    }

    @GetMapping("/signup")
    public String signup() {
        return "signup";
    }

    @PostMapping("/signup")
    public String signup(@RequestParam String username,
                        @RequestParam String password,
                        RedirectAttributes redirectAttributes) {
        try {
            username = username.trim();
            password = password.trim();
            Path usersFile = Paths.get("users.txt");
            List<String> lines = Files.exists(usersFile) ? Files.readAllLines(usersFile) : new ArrayList<>();
            lines.add(username + "," + password);
            Files.write(usersFile, lines);
        } catch (IOException e) {
            redirectAttributes.addFlashAttribute("error", "Failed to create account");
            return "redirect:/signup";
        }
        return "redirect:/login";
    }

    @GetMapping("/logout")
    public String logout(HttpSession session) {
        session.invalidate();
        return "redirect:/login";
    }

    @GetMapping("/upload")
    public String upload(HttpSession session) {
        if (session.getAttribute("user") == null) {
            return "redirect:/login";
        }
        return "upload";
    }

    @PostMapping("/upload")
    public String uploadFile(@RequestParam("file") MultipartFile file,
                           HttpSession session,
                           Model model) {
        String username = (String) session.getAttribute("user");
        if (username == null) {
            return "redirect:/login";
        }

        if (file.isEmpty() || !file.getOriginalFilename().endsWith(".csv")) {
            model.addAttribute("error", "Only .csv files are allowed!");
            return "upload";
        }

        try {
            Path uploadPath = Paths.get(UPLOAD_DIR);
            if (!Files.exists(uploadPath)) {
                Files.createDirectories(uploadPath);
            }

            Path filePath = uploadPath.resolve(file.getOriginalFilename());
            Files.write(filePath, file.getBytes());

            List<Map<String, Object>> results = dropoutAnalysisService.analyzeCSV(filePath);
            model.addAttribute("result", results);
            return "result";

        } catch (IOException e) {
            model.addAttribute("error", "Failed to process file");
            return "upload";
        }
    }

    @GetMapping("/manual-entry")
    public String manualEntry(HttpSession session) {
        if (session.getAttribute("user") == null) {
            return "redirect:/login";
        }
        return "manual_entry";
    }

    @PostMapping("/manual-entry")
    public String manualEntry(@RequestParam Map<String, String> formData,
                            HttpSession session,
                            Model model) {
        String username = (String) session.getAttribute("user");
        if (username == null) {
            return "redirect:/login";
        }

        Student student = new Student();
        student.setUsername(username);
        student.setStudName(formData.get("stud_name"));
        student.setGender(formData.get("gender"));
        student.setDob(formData.get("dob"));
        student.setStatus(formData.get("status"));
        student.setSslcMarks(formData.get("sslc_marks"));
        student.setHscMarks(formData.get("hsc_marks"));
        student.setClgName(formData.get("clg_name"));
        student.setMotherName(formData.get("mother_name"));
        student.setFatherName(formData.get("father_name"));
        student.setAddress(formData.get("address"));

        studentRepository.save(student);

        Map<String, Object> result = dropoutAnalysisService.analyzeManualEntry(formData);
        model.addAttribute("result", result);
        return "result";
    }

    @GetMapping("/update-marks")
    public String updateMarks(HttpSession session, Model model) {
        String username = (String) session.getAttribute("user");
        if (username == null) {
            return "redirect:/login";
        }

        List<Student> students = studentRepository.findByUsername(username);
        model.addAttribute("students", students);
        return "update_marks";
    }

    @PostMapping("/update-marks")
    public String updateMarks(@RequestParam Long student_id,
                            @RequestParam Integer semester,
                            @RequestParam String stage,
                            @RequestParam Map<String, String> formData,
                            HttpSession session,
                            RedirectAttributes redirectAttributes) {
        String username = (String) session.getAttribute("user");
        if (username == null) {
            return "redirect:/login";
        }

        Student student = studentRepository.findByIdAndUsername(student_id, username);
        if (student == null) {
            redirectAttributes.addFlashAttribute("error", "Student not found");
            return "redirect:/update-marks";
        }

        UniversityMarks marks = universityMarksRepository.findByStudentIdAndSemester(student_id, semester);
        if (marks == null) {
            marks = new UniversityMarks();
            marks.setStudent(student);
            marks.setSemester(semester);
        }

        if ("internal1".equals(stage)) {
            if (marks.getInternal1Sub1() != null) {
                redirectAttributes.addFlashAttribute("error", "Internal 1 marks already updated for this student and semester.");
                return "redirect:/update-marks";
            }
            marks.setInternal1Sub1(parseDouble(formData.get("sub1")));
            marks.setInternal1Sub2(parseDouble(formData.get("sub2")));
            marks.setInternal1Sub3(parseDouble(formData.get("sub3")));
            marks.setInternal1Sub4(parseDouble(formData.get("sub4")));
            marks.setInternal1Sub5(parseDouble(formData.get("sub5")));
            marks.setInternal1Sub6(parseDouble(formData.get("sub6")));
        } else if ("internal2".equals(stage)) {
            marks.setInternal2Sub1(parseDouble(formData.get("sub1")));
            marks.setInternal2Sub2(parseDouble(formData.get("sub2")));
            marks.setInternal2Sub3(parseDouble(formData.get("sub3")));
            marks.setInternal2Sub4(parseDouble(formData.get("sub4")));
            marks.setInternal2Sub5(parseDouble(formData.get("sub5")));
            marks.setInternal2Sub6(parseDouble(formData.get("sub6")));
        } else if ("internal3".equals(stage)) {
            marks.setInternal3Sub1(parseDouble(formData.get("sub1")));
            marks.setInternal3Sub2(parseDouble(formData.get("sub2")));
            marks.setInternal3Sub3(parseDouble(formData.get("sub3")));
            marks.setInternal3Sub4(parseDouble(formData.get("sub4")));
            marks.setInternal3Sub5(parseDouble(formData.get("sub5")));
            marks.setInternal3Sub6(parseDouble(formData.get("sub6")));
        } else if ("cgpa".equals(stage)) {
            marks.setCgpa(parseDouble(formData.get("cgpa")));
        }

        universityMarksRepository.save(marks);
        redirectAttributes.addFlashAttribute("success", "Marks updated!");
        return "redirect:/update-marks";
    }

    @GetMapping("/all-students")
    public String allStudents(HttpSession session, Model model) {
        String username = (String) session.getAttribute("user");
        if (username == null) {
            return "redirect:/login";
        }

        List<Student> students = studentRepository.findByUsername(username);
        model.addAttribute("students", students);
        return "all_students";
    }

    @GetMapping("/dropout-students")
    public String dropoutStudents(HttpSession session, Model model) {
        String username = (String) session.getAttribute("user");
        if (username == null) {
            return "redirect:/login";
        }

        List<Student> students = studentRepository.findByUsername(username);

        // Get dropout students with details
        List<Map<String, Object>> dropoutStudents = new ArrayList<>();
        Map<Long, DropoutStudentDetails> dropoutDetailsMap = new HashMap<>();

        List<DropoutStudentDetails> allDropoutDetails = dropoutStudentDetailsRepository.findAll();
        for (DropoutStudentDetails details : allDropoutDetails) {
            dropoutDetailsMap.put(details.getStudent().getId(), details);
        }

        for (Student student : students) {
            DropoutStudentDetails details = dropoutDetailsMap.get(student.getId());
            if (details != null) {
                Map<String, Object> dropoutStudent = new HashMap<>();
                dropoutStudent.put("student", student);
                dropoutStudent.put("details", details);
                dropoutStudents.add(dropoutStudent);
            }
        }

        // Calculate college counts
        Map<String, Integer> collegeCounts = new HashMap<>();
        for (Map<String, Object> dropoutStudent : dropoutStudents) {
            Student student = (Student) dropoutStudent.get("student");
            String college = student.getClgName() != null ? student.getClgName() : "Unknown";
            collegeCounts.put(college, collegeCounts.getOrDefault(college, 0) + 1);
        }

        model.addAttribute("students", students);
        model.addAttribute("dropoutStudents", dropoutStudents);
        model.addAttribute("collegeCounts", collegeCounts);
        return "dropout_students";
    }

    @PostMapping("/dropout-students")
    public String saveDropoutDetails(@RequestParam Map<String, String> formData,
                                   HttpSession session,
                                   RedirectAttributes redirectAttributes) {
        String username = (String) session.getAttribute("user");
        if (username == null) {
            return "redirect:/login";
        }

        Long studentId = Long.parseLong(formData.get("student_id"));
        Student student = studentRepository.findByIdAndUsername(studentId, username);
        if (student == null) {
            return "redirect:/dropout-students";
        }

        DropoutStudentDetails details = dropoutStudentDetailsRepository.findByStudentId(studentId);
        if (details == null) {
            details = new DropoutStudentDetails();
            details.setStudent(student);
        }

        details.setDisciplinaryAction("yes".equals(formData.get("disciplinary_action")));
        details.setFamilyIncome(formData.get("family_income"));
        details.setFeesPaymentStatus(formData.get("fees_payment_status"));
        details.setEducationalLoad("yes".equals(formData.get("educational_load")));
        details.setPartTimeWork("yes".equals(formData.get("part_time_work")));
        details.setHealthIssue("yes".equals(formData.get("health_issue")));
        details.setHealthIssueDescription(formData.get("health_issue_description"));
        details.setDayScholarOrHosteller(formData.get("day_scholar_or_hosteller"));

        dropoutStudentDetailsRepository.save(details);

        // Update student status to dropout
        student.setStatus("dropout");
        studentRepository.save(student);

        redirectAttributes.addFlashAttribute("success", "Dropout details saved and graph updated successfully.");
        return "redirect:/dropout-students?student_id=" + studentId;
    }

    @GetMapping("/stats")
    public String stats(HttpSession session) {
        if (session.getAttribute("user") == null) {
            return "redirect:/login";
        }
        return "stats";
    }

    @GetMapping("/dropout-details")
    public String dropoutDetails(HttpSession session, Model model) {
        String username = (String) session.getAttribute("user");
        if (username == null) {
            return "redirect:/login";
        }

        List<Student> students = studentRepository.findByUsername(username);
        List<Map<String, Object>> dropoutStudents = new ArrayList<>();
        Map<Long, DropoutStudentDetails> dropoutDetailsMap = new HashMap<>();

        List<DropoutStudentDetails> allDropoutDetails = dropoutStudentDetailsRepository.findAll();
        for (DropoutStudentDetails details : allDropoutDetails) {
            dropoutDetailsMap.put(details.getStudent().getId(), details);
        }

        for (Student student : students) {
            DropoutStudentDetails details = dropoutDetailsMap.get(student.getId());
            if (details != null) {
                Map<String, Object> dropoutStudent = new HashMap<>();
                dropoutStudent.put("student", student);
                dropoutStudent.put("details", details);
                dropoutStudents.add(dropoutStudent);
            }
        }

        model.addAttribute("dropoutStudents", dropoutStudents);
        return "dropout_details";
    }

    @GetMapping("/solutions")
    public String solutions(HttpSession session, Model model) {
        String username = (String) session.getAttribute("user");
        if (username == null) {
            return "redirect:/login";
        }

        List<Student> students = studentRepository.findByUsername(username);
        model.addAttribute("students", students);
        return "solutions";
    }

    @PostMapping("/solutions")
    public String getSolutions(@RequestParam Long student_id,
                             HttpSession session,
                             Model model) {
        String username = (String) session.getAttribute("user");
        if (username == null) {
            return "redirect:/login";
        }

        Student selectedStudent = studentRepository.findByIdAndUsername(student_id, username);
        DropoutStudentDetails dropoutDetails = dropoutStudentDetailsRepository.findByStudentId(student_id);

        Map<String, Object> dropoutDetailsMap = new HashMap<>();
        if (dropoutDetails != null) {
            dropoutDetailsMap.put("disciplinary_action", dropoutDetails.getDisciplinaryAction());
            dropoutDetailsMap.put("family_income", dropoutDetails.getFamilyIncome());
            dropoutDetailsMap.put("fees_payment_status", dropoutDetails.getFeesPaymentStatus());
            dropoutDetailsMap.put("educational_load", dropoutDetails.getEducationalLoad());
            dropoutDetailsMap.put("part_time_work", dropoutDetails.getPartTimeWork());
            dropoutDetailsMap.put("health_issue", dropoutDetails.getHealthIssue());
            dropoutDetailsMap.put("health_issue_description", dropoutDetails.getHealthIssueDescription());
            dropoutDetailsMap.put("day_scholar_or_hosteller", dropoutDetails.getDayScholarOrHosteller());
        }

        List<Student> students = studentRepository.findByUsername(username);
        model.addAttribute("students", students);
        model.addAttribute("selected_student", selectedStudent);
        model.addAttribute("dropout_details", dropoutDetailsMap);
        return "solutions";
    }

    @GetMapping("/about")
    public String about(HttpSession session) {
        if (session.getAttribute("user") == null) {
            return "redirect:/login";
        }
        return "about";
    }

    @GetMapping("/contact")
    public String contact(HttpSession session) {
        if (session.getAttribute("user") == null) {
            return "redirect:/login";
        }
        return "contact";
    }

    private Double parseDouble(String value) {
        if (value == null || value.trim().isEmpty()) {
            return 0.0;
        }
        try {
            return Double.parseDouble(value);
        } catch (NumberFormatException e) {
            return 0.0;
        }
    }
}
