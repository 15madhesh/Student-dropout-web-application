package com.example.dropoutanalyzer.repository;

import com.example.dropoutanalyzer.model.UniversityMarks;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface UniversityMarksRepository extends JpaRepository<UniversityMarks, Long> {

    List<UniversityMarks> findByStudentId(Long studentId);

    UniversityMarks findByStudentIdAndSemester(Long studentId, Integer semester);

}
