# Оптимизированный CI/CD пайплайн для приложения "Hello, World" на Kubernetes

Этот репозиторий демонстрирует создание и оптимизацию CI/CD пайплайна для простого Python приложения "Hello, World", развернутого в кластере Kubernetes (Minikube).  Пайплайн использует GitLab CI/CD, Docker, Helm, Terraform, Prometheus и Grafana для мониторинга.

## Архитектура

![Архитектура](architecture.png)  *(Добавь сюда схему архитектуры)*

* **Приложение:** Простое веб-приложение на Flask (Python), возвращающее "Hello, World!".
* **Docker:**  Приложение упаковано в Docker-образ.
* **Kubernetes (Minikube):**  Приложение развертывается в кластере Minikube.
* **Helm:**  Используется для управления развертыванием приложения в Kubernetes.
* **Terraform:**  Используется для управления инфраструктурой (Minikube).
* **GitLab CI/CD:**  Оркестрирует все этапы пайплайна (сборка, тестирование, развертывание).
* **Prometheus:**  Собирает метрики приложения и пайплайна.
* **Grafana:** Визуализирует метрики, собранные Prometheus.
* **Flagger:** Автоматизирует canary deployment.

## Оптимизации

В этом пайплайне применены следующие оптимизации:

* **Многоступенчатая сборка Docker:**  Уменьшает размер финального образа и ускоряет сборку.
* **Кэширование зависимостей:**  Сохраняет зависимости Python между запусками пайплайна, ускоряя сборку.
* **Параллелизация тестов:**  Запускает тесты параллельно, сокращая общее время тестирования.
* **Инфраструктура как код (Terraform):**  Автоматизирует управление инфраструктурой, делая деплой более предсказуемым и повторяемым.
* **Canary deployments (Flagger):** Позволяет постепенно выкатывать новые версии приложения, снижая риски.
* **Мониторинг (Prometheus & Grafana):** Предоставляет метрики для анализа производительности приложения и пайплайна.

## Инструкция по запуску

1. **Предварительные требования:**
    * Установленные `kubectl`, `helm`, `docker`, `terraform`, `minikube`.
    * Аккаунт на GitLab.com.
    * Запущенный Minikube: `minikube start`

2. **Клонирование репозитория:**
```bash
git clone https://gitlab.com/mikhailde/my-app.git
cd my-app
```
3. **Развертывание приложения:**
    * **Через Helm:**
        * ```bash
          helm upgrade --install my-app ./chart \
            --set image.tag=latest \
            --set image.repository=$CI_REGISTRY_IMAGE \
            --namespace my-app --create-namespace
          ```
    * **Через Terraform:**
        * ```bash
            cd terraform
            terraform init
            terraform apply -auto-approve -var="image_registry=$CI_REGISTRY_IMAGE" -var="image_tag=latest"
          ```
4. **Доступ к приложению:**
```bash
minikube service my-app --url
```

5. **Доступ к Grafana:**
```bash
kubectl port-forward service/grafana 3000:80
```
Открой в браузере: `http://localhost:3000` (admin/prom-operator).
Импортируй дашборды `grafana/app_preformance.json` и `grafana/cicd.json`

## Структура репозитория

* `app.py`: Код приложения.
* `chart/`: Helm чарт для приложения.
* `Dockerfile`: Dockerfile для сборки образа.
* `grafana/`: JSON файлы с дашбордами Grafana.
* `k8s/`: Файлы манифестов Kubernetes.
* `requirements.txt`: Зависимости Python.
* `terraform/`: Terraform код для управления инфраструктурой.
* `tests/`: Юнит-тесты для приложения.

## Результаты и метрики

*(Добавь сюда скриншоты дашбордов Grafana с метриками производительности приложения и пайплайна)*

## Дальнейшие шаги

* **Автоматизация canary deployments с Flagger:**  Интеграция Flagger в пайплайн для автоматизации canary deployments.
* **Более сложные сценарии:**  Добавление этапов для интеграционного и end-to-end тестирования, security сканирования, и т.д.
* **Оптимизация использования ресурсов:** Настройка requests и limits для ресурсов pod'ов.

## Заключение

Этот проект демонстрирует базовые принципы оптимизации CI/CD пайплайна.  Он может быть использован в качестве основы для построения более сложных и эффективных пайплайнов.