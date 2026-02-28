package com.example.dropoutanalyzer.controller;

import com.example.dropoutanalyzer.model.Student;
import com.example.dropoutanalyzer.model.UniversityMarks;
import com.example.dropoutanalyzer.repository.StudentRepository;
import com.example.dropoutanalyzer.repository.UniversityMarksRepository;
import com.example.dropoutanalyzer.repository.DropoutStudentDetailsRepository;
import com.example.dropoutanalyzer.service.DropoutAnalysisService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import javax.servlet.http.HttpSession;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api")
public class ApiController {

    @Autowired
    private StudentRepository studentRepository;

    @Autowired
    private UniversityMarksRepository universityMarksRepository;

    @Autowired
    private DropoutStudentDetailsRepository dropoutStudentDetailsRepository;

    @Autowired
    private DropoutAnalysisService dropoutAnalysisService;

    @Autowired
    private RestTemplate restTemplate;

    @GetMapping("/news")
    public ResponseEntity<List<Map<String, Object>>> getNews() {
        List<Map<String, Object>> newsItems = Arrays.asList(
            Map.of("title", "Student drops out to start tea business, earns ₹5 crore/year",
                   "url", "https://www.news18.com/viral/dropout-chaiwala",
                   "image", "/static/images/news1.jpeg",
                   "date", "2025-07-20"),
            Map.of("title", "Rising dropout rates concern educators nationwide",
                   "url", "https://timesofindia.indiatimes.com/topic/dropout-of-students",
                   "image", "/static/images/news2.jpeg",
                   "date", "2025-07-18"),
            Map.of("title", "University introduces new program to retain students",
                   "url", "https://www.hindustantimes.com/education/retention-program",
                   "image", "/static/images/news3.jpeg",
                   "date", "2025-07-15"),
            Map.of("title", "Government announces scholarship for at-risk students",
                   "url", "https://www.thehindu.com/search/#gsc.tab=0&gsc.q=dropout%20of%20students&gsc.sort=",
                   "image", "/static/images/news4.jpeg",
                   "date", "2025-07-12"),
            Map.of("title", "Study links extracurriculars to lower dropout rates",
                   "url", "https://indianexpress.com/education-study",
                   "image", "/static/images/news5.jpeg",
                   "date", "2025-07-10"),
            Map.of("title", "College dropout builds edtech startup",
                   "url", "https://economictimes.com/success-story",
                   "image", "/static/images/news6.jpeg",
                   "date", "2025-07-08"),
            Map.of("title", "Alumni mentorship program reduces dropouts by 25%",
                   "url", "https://www.deccanchronicle.com/mentorship-impact",
                   "image", "/static/images/news7.jpeg",
                   "date", "2025-07-05"),
            Map.of("title", "Rural schools face increasing student attrition",
                   "url", "https://www.thequint.com/rural-education",
                   "image", "/static/images/news8.jpeg",
                   "date", "2025-07-03"),
            Map.of("title", "Online learning contributing to dropout crisis?",
                   "url", "https://www.firstpost.com/online-education-impact",
                   "image", "/static/images/news9.jpeg",
                   "date", "2025-06-30"),
            Map.of("title", "Vocational training helps retain disengaged students",
                   "url", "https://www.financialexpress.com/vocational-success",
                   "image", "/static/images/news10.jpeg",
                   "date", "2025-06-28"),
            Map.of("title", "Celebrity funds scholarship for dropout prevention",
                   "url", "https://www.mid-day.com/celebrity-scholarship",
                   "image", "/static/images/news11.jpeg",
                   "date", "2025-06-25"),
            Map.of("title", "New app connects at-risk students with counselors",
                   "url", "https://www.livemint.com/edtech-app",
                   "image", "/static/images/news12.jpeg",
                   "date", "2025-06-22")
        );

        return ResponseEntity.ok(newsItems);
    }

    @GetMapping("/stats")
    public ResponseEntity<Map<String, Object>> getStats(HttpSession session) {
        String username = (String) session.getAttribute("user");
        if (username == null) {
            return ResponseEntity.status(401).body(Map.of("error", "Unauthorized"));
        }

        List<Student> students = studentRepository.findByUsername(username);

        // Gender stats (only for dropout students)
        Map<String, Integer> genderCounts = new HashMap<>();
        Map<String, Integer> stateCounts = new HashMap<>();
        Map<String, Integer> collegeCounts = new HashMap<>();
        Map<String, Integer> ageCounts = new HashMap<>();

        for (Student student : students) {
            // Only include dropout students in gender stats
            if ("dropout".equals(student.getStatus())) {
                String gender = student.getGender() != null ? student.getGender() : "Unknown";
                genderCounts.put(gender, genderCounts.getOrDefault(gender, 0) + 1);
            }

            // State stats (from address)
            String address = student.getAddress() != null ? student.getAddress() : "";
            String state = address.contains(",") ? address.substring(address.lastIndexOf(",") + 1).trim() : "Unknown";
            stateCounts.put(state, stateCounts.getOrDefault(state, 0) + 1);

            // College stats
            String college = student.getClgName() != null ? student.getClgName() : "Unknown";
            collegeCounts.put(college, collegeCounts.getOrDefault(college, 0) + 1);

            // Age stats (from dob if available)
            if (student.getDob() != null) {
                try {
                    LocalDate dob = LocalDate.parse(student.getDob(), DateTimeFormatter.ofPattern("yyyy-MM-dd"));
                    int age = LocalDate.now().getYear() - dob.getYear();
                    String ageGroup = (age / 5 * 5) + "-" + (age / 5 * 5 + 4);
                    ageCounts.put(ageGroup, ageCounts.getOrDefault(ageGroup, 0) + 1);
                } catch (Exception e) {
                    ageCounts.put("Unknown", ageCounts.getOrDefault("Unknown", 0) + 1);
                }
            }
        }

        Map<String, Object> response = new HashMap<>();
        response.put("genderData", Map.of(
            "labels", new ArrayList<>(genderCounts.keySet()),
            "values", new ArrayList<>(genderCounts.values())
        ));
        response.put("stateData", Map.of(
            "labels", new ArrayList<>(stateCounts.keySet()),
            "values", new ArrayList<>(stateCounts.values())
        ));
        response.put("collegeData", Map.of(
            "labels", new ArrayList<>(collegeCounts.keySet()),
            "values", new ArrayList<>(collegeCounts.values())
        ));
        response.put("ageData", Map.of(
            "labels", new ArrayList<>(ageCounts.keySet()),
            "values", new ArrayList<>(ageCounts.values())
        ));

        return ResponseEntity.ok(response);
    }

    @GetMapping("/student-marks/{studentId}")
    public ResponseEntity<Map<String, Object>> getStudentMarks(@PathVariable Long studentId, HttpSession session) {
        String username = (String) session.getAttribute("user");
        if (username == null) {
            return ResponseEntity.status(401).body(Map.of("error", "Unauthorized"));
        }

        Student student = studentRepository.findByIdAndUsername(studentId, username);
        if (student == null) {
            return ResponseEntity.status(404).body(Map.of("error", "Student not found"));
        }

        List<UniversityMarks> marks = universityMarksRepository.findByStudentId(studentId);
        List<Map<String, Double>> marksList = marks.stream().map(mark -> {
            Map<String, Double> markMap = new HashMap<>();
            markMap.put("semester", mark.getSemester().doubleValue());
            if (mark.getInternal1Sub1() != null) markMap.put("internal1_sub1", mark.getInternal1Sub1());
            if (mark.getInternal1Sub2() != null) markMap.put("internal1_sub2", mark.getInternal1Sub2());
            if (mark.getInternal1Sub3() != null) markMap.put("internal1_sub3", mark.getInternal1Sub3());
            if (mark.getInternal1Sub4() != null) markMap.put("internal1_sub4", mark.getInternal1Sub4());
            if (mark.getInternal1Sub5() != null) markMap.put("internal1_sub5", mark.getInternal1Sub5());
            if (mark.getInternal1Sub6() != null) markMap.put("internal1_sub6", mark.getInternal1Sub6());
            if (mark.getInternal2Sub1() != null) markMap.put("internal2_sub1", mark.getInternal2Sub1());
            if (mark.getInternal2Sub2() != null) markMap.put("internal2_sub2", mark.getInternal2Sub2());
            if (mark.getInternal2Sub3() != null) markMap.put("internal2_sub3", mark.getInternal2Sub3());
            if (mark.getInternal2Sub4() != null) markMap.put("internal2_sub4", mark.getInternal2Sub4());
            if (mark.getInternal2Sub5() != null) markMap.put("internal2_sub5", mark.getInternal2Sub5());
            if (mark.getInternal2Sub6() != null) markMap.put("internal2_sub6", mark.getInternal2Sub6());
            if (mark.getInternal3Sub1() != null) markMap.put("internal3_sub1", mark.getInternal3Sub1());
            if (mark.getInternal3Sub2() != null) markMap.put("internal3_sub2", mark.getInternal3Sub2());
            if (mark.getInternal3Sub3() != null) markMap.put("internal3_sub3", mark.getInternal3Sub3());
            if (mark.getInternal3Sub4() != null) markMap.put("internal3_sub4", mark.getInternal3Sub4());
            if (mark.getInternal3Sub5() != null) markMap.put("internal3_sub5", mark.getInternal3Sub5());
            if (mark.getInternal3Sub6() != null) markMap.put("internal3_sub6", mark.getInternal3Sub6());
            if (mark.getCgpa() != null) markMap.put("cgpa", mark.getCgpa());
            return markMap;
        }).collect(Collectors.toList());

        double attendancePercent = 0.0; // Default attendance, could be added to Student model
        double dropoutPercentage = dropoutAnalysisService.calculateDropoutPercentage(marksList, attendancePercent);

        Map<String, Object> response = new HashMap<>();
        response.put("marks", marksList);
        response.put("dropout_percentage", dropoutPercentage);

        return ResponseEntity.ok(response);
    }
}
