package com.example.dropoutanalyzer.service;

import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.core.userdetails.User;
import org.springframework.stereotype.Service;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

@Service
public class CustomUserDetailsService implements UserDetailsService {

    private static final String USERS_FILE = "users.txt";

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        try {
            Path usersFile = Path.of(USERS_FILE);
            if (Files.exists(usersFile)) {
                List<String> lines = Files.readAllLines(usersFile);
                for (String line : lines) {
                    String[] parts = line.trim().split(",", 2);
                    if (parts.length == 2) {
                        String fileUsername = parts[0].trim();
                        String filePassword = parts[1].trim();
                        if (fileUsername.equals(username)) {
                            // Trim username and password before returning
                            return User.withUsername(fileUsername)
                                    .password(filePassword)
                                    .authorities(new ArrayList<>())
                                    .build();
                        }
                    }
                }
            }
        } catch (Exception e) {
            throw new UsernameNotFoundException("Error reading users file", e);
        }
        throw new UsernameNotFoundException("User not found: " + username);
    }
}
