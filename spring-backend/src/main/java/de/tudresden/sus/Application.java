package de.tudresden.sus;

import com.fasterxml.jackson.databind.ObjectMapper;
import de.tudresden.sus.adapter.outbound.entity.Project;
import de.tudresden.sus.adapter.inbound.dto.ProjectDTO;
import de.tudresden.sus.adapter.outbound.entity.Track;
import lombok.RequiredArgsConstructor;
import org.modelmapper.ModelMapper;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.util.ArrayList;

@SpringBootApplication
@RequiredArgsConstructor
public class Application {


	@Bean
	public ModelMapper modelMapper() {
		var mapper = new ModelMapper();
		return mapper;
	}

	@Bean
	public ObjectMapper objectMapper() {
		// customize object mapper here
		return new ObjectMapper();
	}

	public static void main(String[] args) {
		SpringApplication.run(Application.class, args);
	}

}
