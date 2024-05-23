package com.example.intellimatch.service;

import com.example.intellimatch.model.SurveySection;
import com.example.intellimatch.repository.SurveySectionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class SurveySectionService {

    private final SurveySectionRepository surveySectionRepository;

    @Autowired
    public SurveySectionService(SurveySectionRepository surveySectionRepository) {
        this.surveySectionRepository = surveySectionRepository;
    }

    public List<SurveySection> getAllSurveySections() {
        return surveySectionRepository.findAll();
    }

    public Optional<SurveySection> getSurveySectionById(Integer sectionId) {
        return surveySectionRepository.findById(sectionId);
    }

    public void saveSurveySection(SurveySection surveySection) {
        surveySectionRepository.save(surveySection);
    }

    public void deleteSurveySection(Integer sectionId) {
        surveySectionRepository.deleteById(sectionId);
    }
}
