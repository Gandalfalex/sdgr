FROM maven:3.8.5-openjdk-17 as builder

WORKDIR /app
COPY . .
RUN mvn package -Pnative -DskipTests


FROM maven:3.8.5-openjdk-17 as runner
WORKDIR /app
COPY --from=builder /app/target/sus.jar sus.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/sus.jar"]