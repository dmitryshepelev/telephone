ALTER TABLE "main_app_userprofile" ADD COLUMN "secret_key" varchar(30) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "secret_key" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "user_code" TYPE varchar(30);