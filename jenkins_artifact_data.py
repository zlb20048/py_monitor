class JenkinsArtifactData:
    def __init__(self, name, build_url, artifact_url, build_time, build_content):
        self.name = name
        self.build_url = build_url
        self.artifact_url = artifact_url
        self.build_time = build_time
        self.build_content = build_content
