package de.tudresden.sus.adapter.inbound.rest;

import de.tudresden.sus.adapter.inbound.dto.UserDTO;
import de.tudresden.sus.adapter.outbound.entity.User;
import de.tudresden.sus.aop.AttachUser;
import de.tudresden.sus.aop.UserAspect;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/user")
@Slf4j
@CrossOrigin
@RequiredArgsConstructor
public class UserController {

    @GetMapping
    @AttachUser
    public ResponseEntity<UserDTO> getUserDRTO(){
        User user = UserAspect.getCurrentUser();
        return ResponseEntity.ok().body(new UserDTO().setMail(user.getEmail()).setName(user.getFirstName()));
    }
}
