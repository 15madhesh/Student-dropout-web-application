package com.example.dropoutanalyzer.repository;

import com.example.dropoutanalyzer.model.Student;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface StudentRepository extends JpaRepository<Student, Long> {

    List<Student> findByUsername(String username);

    Student findByIdAndUsername(Long id, String username);

}
