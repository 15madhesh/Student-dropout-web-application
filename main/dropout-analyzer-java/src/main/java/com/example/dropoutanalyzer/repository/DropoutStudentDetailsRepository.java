package com.example.dropoutanalyzer.repository;

import com.example.dropoutanalyzer.model.DropoutStudentDetails;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DropoutStudentDetailsRepository extends JpaRepository<DropoutStudentDetails, Long> {

    DropoutStudentDetails findByStudentId(Long studentId);

}
